
import os
import datetime
# Firebase Imports
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import exceptions
# PySide2 Imports
from PySide2.QtCore import QDateTime, Slot, QObject
from AttnSignal import AttnSignal

class SignInOut(QObject):
    Season = "Season2021-2022"
    AttnHistory = "AttnHistory"
    History = "History"
    SignIn = "SignIn"
    SignOut = "SignOut"
    LastScan = "LastScan"
    AlreadySignOut = "Sorry, You have already been signed out!"
    Hours22 = 22*60*60

    def __init__(self):
        self.cred = credentials.Certificate(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))
        firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()
        self.reportstatus = AttnSignal()

    def processSignInOut(self, name, attnhistory):
        utcnow = QDateTime().currentDateTimeUtc()
        now = utcnow.toLocalTime()
        signdatetime = utcnow.toPython()
        signtype = self.SignIn

        # get the document snapshot
        docSnapshot = attnhistory.document(self.History).get()
        logdate = "Log" + "{}{}{}".format(now.date().month(),now.date().day(),now.date().year())
        if not docSnapshot.exists:
            # No Season document
            attnhistory.document(self.History).set({
                self.LastScan : {
                    signtype : logdate
                },
                logdate : {
                    signtype : signdatetime
                }
            })
            self.reportstatus.signal.emit(name, signtype)
        else:
            # Season document exist
            data = docSnapshot.to_dict()
            # empty dictionary - no data
            if data:
                # check for LastScan field
                if self.LastScan in data.keys():
                    lastScanData = docSnapshot.get(self.LastScan)
                    # has LastScan data
                    if lastScanData:
                        if (list(lastScanData)[0] == self.SignIn):
                            lastSignInData = docSnapshot.get(lastScanData[self.SignIn] + "." + self.SignIn)
                            # calculate if signout is within 22 hours
                            prevsignin = datetime.datetime(lastSignInData.year, lastSignInData.month, lastSignInData.day, lastSignInData.hour, lastSignInData.minute, lastSignInData.second)
                            delta = signdatetime - prevsignin
                            if (delta.total_seconds() < self.Hours22):
                                logdate = lastScanData[self.SignIn]
                                signtype = self.SignOut
                            else:
                                signtype = self.SignIn
            try:
                lastSignOutData = docSnapshot.get(logdate + "." + self.SignOut)
                signtype = self.AlreadySignOut
            except KeyError:
                docref = attnhistory.document(self.History)
                docref.update({
                    logdate + "." + signtype : signdatetime
                })
                if (signtype == self.SignIn):
                    docref.update({
                        self.LastScan : {
                            signtype : logdate
                        }
                    })
                else:
                    docref.update({
                        self.LastScan : {}
                    })
            self.reportstatus.signal.emit(name, signtype)

    @Slot(str)
    def process(self, rfid):
        print(rfid)
        if rfid == '':
            return
        docref = self.db.collection(self.Season).document(rfid)
        try:
            doc = docref.get()
            if doc.exists:
                name = doc.get(u'First') + " " + doc.get(u'Last')
                attnhistory = docref.collection(self.AttnHistory)
                if attnhistory is not None:
                    # now process sign in and sign out
                    self.processSignInOut(name, attnhistory)
            else:
                self.reportstatus.signal.emit("RFID # unassigned", "")
        except exceptions.NotFound:
            print("No AttnHistory document found for " + name )

""" For local debugging only """
if __name__ == "__main__":
    signinout = SignInOut()
    signinout.process("3699937085")
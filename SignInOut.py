
import os
import datetime
# Firebase Imports
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import exceptions
# PySide2 Imports
from PySide6.QtCore import QDateTime, Slot, QObject
from AttnSignal import AttnSignal

class SignInOut(QObject):
    Name = "Name"
    Date = "Date"
    Dates = "dates"
    HasSignout = "HasSignOut"
    Meetings = "meetings"
    Members = "members"
    RFIDS = "rfids"
    RFIDTag = "RFIDTag"
    Season = ""
    SignIn = "SignIn"
    SignOut = "SignOut"
    History = "AttnHistory"
    SignInCount = "SignInCount"
    Hours22 = 22*60*60

    def __init__(self, season):
        self.cred = credentials.Certificate(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))
        firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()
        self.reportstatus = AttnSignal()
        self.Season = season

    def processSignInOut(self, rfid, name):
        utcnow = QDateTime().currentDateTimeUtc()
        now = utcnow.toLocalTime()
        signdatetime = utcnow.toPython()
        signtype = self.SignIn

        # get the document snapshot
        colref = self.db.collection(self.Season, self.Meetings, self.Dates)
        logdate = "{:02d}{:02d}{}".format(now.date().month(),now.date().day(),now.date().year())
        docname = rfid + "_" + logdate
        results = colref.where(self.RFIDTag, '==', rfid).where(self.Date, "==", logdate).get()
        try:
            if len(results) == 0:
                ''' Document does not exist, create the document with SignIn data'''
                docref = colref.document(docname)
                signInCount = 1
                docref.create({
                    self.Date: logdate,
                    self.Name: name,
                    self.RFIDTag: rfid,
                    self.HasSignout: False,
                    self.SignInCount: signInCount,
                    signtype : signdatetime,
                    self.History : {
                        str(signInCount) : {
                            signtype : signdatetime
                        }
                    }
                })
            else: 
                ''' Document already exist, and check for last scan'''
                for doc in results:
                    data = doc.to_dict()
                    hasSignOut = False
                    signInCount = data[self.SignInCount]
                    if doc.id == docname and data[self.HasSignout]:
                        signtype = self.SignIn
                        signInCount = signInCount + 1
                    else:
                        signtype = self.SignOut
                        hasSignOut = True

                    if doc.id == docname and data[self.Date] == logdate:
                        docref = doc.reference
                        docref.update({
                            self.HasSignout: hasSignOut,
                            self.SignInCount: signInCount,
                            signtype: signdatetime,
                            self.History + "." + 
                                str(signInCount) + "." + signtype : signdatetime
                        })
            self.reportstatus.signal.emit(name, signtype)
        except ValueError:
            print('value error')

    @Slot(str)
    def process(self, rfid):
        print(rfid)
        if rfid == '':
            return
        colref = self.db.collection(self.Season, self.Members, self.RFIDS)
        docref = colref.document(rfid)
        try:
            doc = docref.get()
            if doc.exists:
                name = doc.get(u'First') + " " + doc.get(u'Last')
                # now process sign in and sign out
                self.processSignInOut(rfid, name)
            else:
                self.reportstatus.signal.emit("RFID # unassigned", "")
        except exceptions.NotFound:
            print("No AttnHistory document found for " + name )

""" For local debugging only """
if __name__ == "__main__":
    signinout = SignInOut()
    signinout.process("3699761165")
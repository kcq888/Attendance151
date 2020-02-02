
import os
import datetime
# Firebase Imports
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import storage, exceptions
# PySide2 Imports
from PySide2 import QtCore
from PySide2.QtCore import QDateTime, QTimeZone, Signal, Slot, QObject
from AttnSignal import AttnSignal

class SignInOut(QObject):
    LastScan = "LastScan"
    Season = "Season"
    SignIn = "SignIn"
    SignOut = "SignOut"
    AlreadySignOut = "Sorry, You have already been signed out!"
    Members = "members"
    AppConfig = "AppConfig"
    AttnHistory = "AttnHistory"
    Hours22 = 22*60*60

    def __init__(self):
        self.cred = credentials.Certificate(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))
        firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()

        # Get the Season document name from the AppConfig
        appconfig = self.db.collection(self.Members).document(self.AppConfig).get()
        self.season = appconfig.get(self.Season)
        self.reportstatus = AttnSignal()
        self.reportname = AttnSignal()

    def processSignInOut(self, attnhistory):
        utcnow = QDateTime().currentDateTimeUtc()
        now = utcnow.toLocalTime()
        signdatetime = utcnow.toPython()

        # get the document snapshot
        docSnapshot = attnhistory.document(self.season).get()
        if not docSnapshot.exists:
            signtype = self.SignIn
            logdate = "Log" + "{}{}{}".format(now.date().month(),now.date().day(),now.date().year())
            attnhistory.document(self.season).set({
                self.LastScan : {
                    signtype : logdate
                },
                logdate : {
                    signtype : signdatetime
                }
            })
            self.reportstatus.signal.emit(signtype)
        else:
            data = docSnapshot.to_dict()
            if self.LastScan in data.keys():
                print(data)
                data = docSnapshot.get(self.LastScan)
                if not data:
                    logdate = "Log" + "{}{}{}".format(now.date().month(),now.date().day(),now.date().year())
                else:
                    if (list(data)[0] == self.SignIn):
                        logdate = data[self.SignIn]
                try:
                    data = docSnapshot.get(logdate + "." + self.SignIn)
                    prevsignin = datetime.datetime(data.year, data.month, data.day, data.hour, data.minute, data.second)
                    delta = signdatetime - prevsignin
                    if (delta.total_seconds() < self.Hours22):
                        signtype = self.SignOut
                    else:
                        signtype = self.SignIn                        
                except KeyError:
                    signtype = self.SignIn
                try:
                    data = docSnapshot.get(logdate + "." + self.SignOut)
                    signtype = self.AlreadySignOut
                except KeyError:
                    docref = attnhistory.document(self.season)
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
            self.reportstatus.signal.emit(signtype)

    @Slot(str)
    def process(self, rfid):
        print(rfid)
        if rfid == '':
            return
        self.reportstatus.signal.emit(rfid)
        members = self.db.collection(self.Members)
        docref = members.document(rfid)
        try:
            doc = docref.get()
            if (doc.exists):
                name = doc.get(u'First') + " " + doc.get(u'Last')
                self.reportname.signal.emit(name)
                attnhistory = docref.collection(self.AttnHistory)
                if attnhistory is not None:
                    # now process sign in and sign out
                    self.processSignInOut(attnhistory)
            else:
                self.reportstatus.signal.emit("RFID # unassigned")
        except exceptions.NotFound:
            print("No AttnHistory document found for " + name )

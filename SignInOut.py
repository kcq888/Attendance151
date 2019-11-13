
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
    Season = "S2019-2020"
    SignIn = "SignIn"
    SignOut = "SignOut"
    AlreadySignOut = "Sorry, You have already signed out!"
    def __init__(self):
        self.cred = credentials.Certificate("team151attendant-firebase-adminsdk-6n2zi-b3551c705a.json")
        firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()
        self.reportstatus = AttnSignal()
        self.reportname = AttnSignal()
    
    @Slot(str)
    def process(self, rfid):
        print(rfid)
        self.reportstatus.signal.emit(rfid)
        members = self.db.collection(u'members')
        docref = members.document(rfid)
        try:
            doc = docref.get()
            if (doc.exists):
                name = doc.get(u'First') + " " + doc.get(u'Last')
                self.reportname.signal.emit(name)
                attnhistory = docref.collection(u'AttnHistory')
                now = QDateTime().currentDateTimeUtc()
                logdate = "Log" + "{}{}{}".format(now.date().month(),now.date().day(),now.date().year())
                signdatetime = now.toPython()
                if attnhistory is not None:
                    signtype = self.SignIn
                    doc = attnhistory.document(self.Season).get()
                    if not doc.exists:
                        attnhistory.document(self.Season).set({
                            logdate : {
                                signtype : signdatetime
                            }
                        })
                        self.reportstatus.signal.emit(signtype)
                    else:
                        data = doc.get(logdate + "." + self.SignIn)
                        prevsignin = datetime.datetime(data.year, data.month, data.day, data.hour, data.minute, data.second)
                        delta = signdatetime - prevsignin
                        if (delta.total_seconds() < 24*60*60):
                            signtype = self.SignOut
                        else:
                            signtype = self.SignIn
                        try:
                            data = doc.get(logdate + "." + self.SignOut)
                            signtype = self.AlreadySignOut
                        except KeyError:
                            docref = attnhistory.document(self.Season)
                            docref.update({
                                logdate + "." + signtype : signdatetime
                            })
                        self.reportstatus.signal.emit(signtype)
            else:
                self.reportstatus.signal.emit("RFID # unassigned")
        except exceptions.NotFound:
            print("No RFID document found!")

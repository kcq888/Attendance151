import sys
import datetime
# Firebase Imports
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import storage, exceptions
# PySide2 Imports
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QDateTime, QTimeZone, Signal, Slot
# Application Imports
from Attendant import Attendant
from SignInOut import SignInOut
from AttnSignal import AttnSignal

class RfID(QtCore.QThread):
    def __init__(self):
        self.attnsignal = AttnSignal()

    def run(self):
        self.attnsignal.signal.emit("3699761165")
        # with open('/dev/tty0', 'r') as tty:
        #     while True:
        #         RFID_input = tty.readline()
        #         self.signal(RFID_input)

if __name__ == "__main__":
    timesFont = QtGui.QFont("Times", 24, QtGui.QFont.Bold)
    app = QtWidgets.QApplication(sys.argv)
    app.setFont(timesFont)
    attendant = Attendant()
    signinout = SignInOut()
    signinout.reportname.signal.connect(attendant.updateName)
    signinout.reportstatus.signal.connect(attendant.updateStatus)
    attendant.show()
    rfid = RfID()
    rfid.attnsignal.signal.connect(signinout.process)
    rfid.run()
    app.exec_()



import logging
from PySide2 import QtCore
from AttnSignal import AttnSignal

class RfID(QtCore.QThread):
    def __init__(self, parent = None):
        QtCore.QThread.__init__(self, parent)
        self.exiting = False
        self.attnsignal = AttnSignal()

    def run(self):
        #self.attnsignal.signal.emit("3699761165")
        print("Entering thread ...")
        while self.exiting == False:
            print("reading...")
            RFID_input = input()
            logging.debug(RFID_input)
            self.attnsignal.signal.emit(RFID_input)

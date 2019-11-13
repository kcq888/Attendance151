import sys
# PySide2 Imports
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QDateTime, QTimeZone, Signal, Slot
# Application Imports
from Attendant import Attendant

if __name__ == "__main__":
    timesFont = QtGui.QFont("Times", 24, QtGui.QFont.Bold)
    app = QtWidgets.QApplication(sys.argv)
    app.setFont(timesFont)
    attendant = Attendant()
    attendant.show()
    app.exec_()



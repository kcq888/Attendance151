import sys
# PySide2 Imports
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QDateTime, QTimeZone, Signal, Slot
# Application Imports
from Attendant import Attendant

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    attendant = Attendant()
    attendant.showFullScreen()
    attendant.show()
    app.exec_()



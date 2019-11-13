# PySide2 Imports
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QDateTime
# Application Imports
import DigitalClock

class Attendant(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(Attendant, self).__init__(parent)
        pixmap = QtGui.QPixmap("./assets/images/2018_Logo.png")
        pixmap = pixmap.scaled(100, 100)
        imageLabel = QtWidgets.QLabel()
        imageLabel.setPixmap(pixmap)
        team151Label = QtWidgets.QLabel("Team 151 Attendant")
        utc_fmt = "yyyy-MM-ddTHH:mm:ss.zzzZ"
        datetimeLabel = QtWidgets.QLabel(QDateTime().currentDateTime().toString())
        attendeeLabel = QtWidgets.QLabel("Kevin Quan")
        clock = DigitalClock()

        teamInfoLayout = QtWidgets.QVBoxLayout()
        teamInfoLayout.addWidget(team151Label)
        teamInfoLayout.addWidget(clock)

        mainLayout = QtWidgets.QGridLayout()
        mainLayout.rowCount = 3
        mainLayout.columnCount = 2
        mainLayout.addWidget(imageLabel, 0, 0)
        mainLayout.addLayout(teamInfoLayout, 0, 1)
        mainLayout.addWidget(attendeeLabel, 2, 1)

        self.setLayout(mainLayout)
        self.setWindowTitle("151 Attendant")
        clock.show()

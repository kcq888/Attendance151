# PySide2 Imports
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QDateTime, Slot
# Application Imports
from DigitalClock import DigitalClock
from SignInOut import SignInOut

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
        self.attendeeLabel = QtWidgets.QLabel("")
        self.attendeeStatusLabel = QtWidgets.QLabel("Empty")
        clock = DigitalClock()

        self.rfidinput = QtWidgets.QLineEdit()
        self.rfidinput.setFocus()
        self.rfidinput.setFixedWidth(100)
        teamInfoLayout = QtWidgets.QVBoxLayout()
        teamInfoLayout.addWidget(team151Label)
        teamInfoLayout.addWidget(clock)

        memberLayout = QtWidgets.QVBoxLayout()
        memberLayout.addWidget(self.attendeeLabel)
        memberLayout.addWidget(self.attendeeStatusLabel)

        mainLayout = QtWidgets.QGridLayout()
        mainLayout.rowCount = 3
        mainLayout.columnCount = 2
        mainLayout.addWidget(imageLabel, 0, 0)
        mainLayout.addLayout(teamInfoLayout, 0, 1)
        mainLayout.addLayout(memberLayout, 2, 1)
        mainLayout.addWidget(self.rfidinput, 2, 0)
        self.setLayout(mainLayout)
        self.setWindowTitle("151 Attendant")
        clock.show()
        
        self.signinout = SignInOut()
        self.signinout.reportname.signal.connect(self.updateName)
        self.signinout.reportstatus.signal.connect(self.updateStatus)
        self.rfidinput.editingFinished.connect(self.accept)

    @Slot(str)
    def accept(self):
        rfid = self.rfidinput.text()
        self.signinout.process(rfid)
        self.rfidinput.clear()
    
    @Slot(str)
    def updateName(self, name):
        self.attendeeLabel.setText(name)

    @Slot(str)
    def updateStatus(self, status):
        self.attendeeStatusLabel.setText(status)

from PySide2.QtCore import QModelIndex, QObject, Signal, Slot, QThread, Property, Qt
from SignInOut import SignInOut
from AttendantModel import AttendantModel

class Attendant(QObject):
    statusChanged = Signal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.status_ = ""
        self.attendantModel_ = AttendantModel()

        self.signinout = SignInOut()
        self.signinout.reportstatus.signal.connect(self.updateStatus)

    def attendantModel(self):
        return self.attendantModel_

    def get_status(self):
        return self.status_

    def set_status(self, status):
        if (self.status_ != status):
            self.status_ = status
            self.statusChanged.emit(status)

    def addAttendant(self, name, status):
        if self.attendantModel_.isExist(name) == None:
            """ 1. Create the empty row"""
            self.attendantModel_.insertRows(0)
            """ 2. Get the index of the newly created row """
            idx = self.attendantModel_.index(0, 0, QModelIndex())
            """ 3. Set the columns values """
            self.attendantModel_.setData(idx, name, status, Qt.EditRole)
        else:
            self.attendantModel_.updateStatus(name, status)

    @Slot(str)
    def onRfidAccepted(self, rfid):
        self.signinout.process(rfid)

    @Slot(str)
    def updateStatus(self, name, status):
        print("updateStatus: ", status)
        self.set_status(name + " " + status)
        self.addAttendant(name, status)

    status = Property(str, fget=get_status, fset=set_status, notify=statusChanged)
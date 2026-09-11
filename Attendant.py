from PySide6.QtCore import QModelIndex, QObject, Signal, Slot, QThread, Property, Qt
from SignInOut import SignInOut
from AttendantModel import AttendantModel

class Attendant(QObject):
    nameChanged = Signal(str)
    statusChanged = Signal(str)

    def __init__(self, season, parent=None) -> None:
        super().__init__(parent=parent)
        self.name_ = ""
        self.status_ = ""
        self.attendantModel_ = AttendantModel()

        self.signinout = SignInOut(season)
        self.signinout.reportstatus.signal.connect(self.updateStatus)

    def attendantModel(self):
        return self.attendantModel_

    def get_name(self):
        return self.name_

    def set_name(self, name):
        if (self.name_ != name):
            self.name_ = name
            self.nameChanged.emit(name)

    def get_status(self):
        return self.status_

    def set_status(self, status):
        if (self.status_ != status):
            self.status_ = status
            self.statusChanged.emit(status)

    def addAttendant(self, name, status, role="Member"):
        if self.attendantModel_.isExist(name) == None:
            row = self.attendantModel_.rowCount()
            """ 1. Create the empty row at the end of the model """
            self.attendantModel_.insertRows(row)
            """ 2. Get the index of the newly created row """
            idx = self.attendantModel_.index(row, 0, QModelIndex())
            """ 3. Set the columns values """
            self.attendantModel_.setData(idx, name, status, role)
        else:
            self.attendantModel_.updateStatus(name, status, role)

    @Slot(str)
    def onRfidAccepted(self, rfid):
        self.signinout.process(rfid)

    @Slot(str, str, str)
    def updateStatus(self, name, status, role="Member"):
        print("updateStatus: ", status, name, role)
        self.set_name(name)
        self.set_status(status)
        if status == SignInOut.SignIn or status == SignInOut.SignOut:
            self.addAttendant(name, status, role)
        else:
            self.status = status

    @Slot()
    def clearAttendants(self):
        self.attendantModel_.clearAttendants()

    name = Property(str, fget=get_name, fset=set_name, notify=nameChanged)
    status = Property(str, fget=get_status, fset=set_status, notify=statusChanged)
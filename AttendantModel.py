import numpy as np
from PySide2.QtCore import Slot, QAbstractListModel, QModelIndex, Qt

class AttendantModel(QAbstractListModel):
    Name = "Name"
    Status = "Status"

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.member_ = ""
        self.headers = [self.Name, self.Status]
        # two dimentional array
        self.attendants = [[]]

    """ Returns the number of rows the model holds. """
    def rowCount(self, parent=QModelIndex()):
        return len(self.attendants)

    """ Returns the number of columns the model holds. """
    def columnCount(self, parent=QModelIndex()):
        return 2

    """ Depending on the index and role given, return data. If not 
        returning data, return None (PySide equivalent of QT's 
        "invalid QVariant").
    """
    def data(self, index, role=Qt.DisplayRole):
        row = index.row()
        if 0 <= row < self.rowCount():
            if role in self.roleNames():
                name_role = self.roleNames()[role].decode()
                col = self.headers.index(name_role)
                return self.attendants[row][col]

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """ Set the headers to be displayed. """
        if role == Qt.DisplayRole and 0 <= section < len(self.headers):
            return self.headers[section]

    def insertRows(self, position, rows=1, index=QModelIndex()):
        """ Insert a row into the model. """
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)

        for row in range(rows):
            self.attendants.insert(position + row, ["name","status"])
        
        self.endInsertRows()
        return True

    def removeRows(self, position, rows=1, index=QModelIndex()):
        """ Remove a row from the model. """
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        
        del self.attendants[position:position+rows]
        
        self.endRemoveRows()
        return True

    def setData(self, index, name, status, role=Qt.EditRole):
        """ Adjust the data (set it to <value>) depending on the given 
            index and role. 
        """
        if role != Qt.EditRole:
            return False

        if index.isValid() and 0 <= index.row() < len(self.attendants):
            attendant = self.attendants[index.row()]
            attendant[0] = name
            attendant[1] = status
            self.dataChanged.emit(index, index)
            return True
        else:
            return False

    def isExist(self, name):
        """ Find if given name already exist in the attendant list """
        attns = np.array(self.attendants)
        if attns.size == 0:
             return None
        try:
            y, x = np.where(attns == name)
            if not len(y) == 0:
                return y[0]
            else:
                return None
        except:
            return None

    def updateStatus(self, name, status):
        """ Find the name in the array and use the index to update the status"""
        row = self.isExist(name)
        if not row == None:
            self.attendants[row][1] = status
            idx = self.index(row, 0, QModelIndex())
            if idx.isValid:
                self.dataChanged.emit(idx, idx)

    def flags(self, index):
        """ Set the item flags at the given index. Seems like we're 
            implementing this function just to see how it's done, as we 
            manually adjust each tableView to have NoEditTriggers.
        """
        if not index.isValid():
            return Qt.ItemIsEnabled
        return Qt.ItemFlags(QAbstractListModel.flags(self, index) |
                            Qt.ItemIsEditable)

    def roleNames(self):
        roles = {}
        for i, header in enumerate(self.headers):
            roles[Qt.UserRole + i + 1] = header.encode()
        return roles

    def clearAttendants(self):
        self.attendants.clear()

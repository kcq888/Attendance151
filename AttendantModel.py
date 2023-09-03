from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt

class AttendantModel(QAbstractTableModel):
    Name = "Name"
    Status = "Status"

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.member_ = ""
        self.headers = [self.Name, self.Status]
        # two dimentional array
        self.attendants = []

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
        if (role == Qt.DisplayRole):
            cell = self.attendants[index.row()][index.column()]
            return cell

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.headers[section]
            else:
                return str(section)

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
        index = 0
        isFound = False

        for attn in self.attendants:
            index += 1
            if (name in attn):
                isFound = True
                break

        if (isFound):
            return index - 1
        else:
            return None

    def updateStatus(self, name, status):
        """ Find the name in the array and use the index to update the status"""
        row = self.isExist(name)
        if not row == None:
            self.attendants[row][1] = status
            idx = self.index(row, 1, QModelIndex())
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

    def clearAttendants(self):
        self.beginResetModel()
        self.attendants.clear()
        self.endResetModel()

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt, QByteArray, Signal, Property

class AttendantModel(QAbstractTableModel):
    Name = "Name"
    Status = "Status"
    Role = "Role"

    MemberRole = Qt.UserRole + 1
    summaryChanged = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.member_ = ""
        self.headers = [self.Name, self.Status, self.Role]
        # two dimentional array
        self.attendants = []

    def roleNames(self):
        roles = super().roleNames()
        roles[Qt.DisplayRole] = QByteArray(b'display')
        roles[self.MemberRole] = QByteArray(b'memberRole')
        return roles

    """ Returns the number of rows the model holds. """
    def rowCount(self, parent=QModelIndex()):
        return len(self.attendants)

    """ Returns the number of columns the model holds. """
    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)

    """ Depending on the index and role given, return data. If not 
        returning data, return None (PySide equivalent of QT's 
        "invalid QVariant").
    """
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.attendants)) or not (0 <= index.column() < len(self.headers)):
            return None

        if (role == Qt.DisplayRole):
            if 0 <= index.column() < len(self.attendants[index.row()]):
                return self.attendants[index.row()][index.column()]
            return ""
        elif (role == self.MemberRole):
            if len(self.attendants[index.row()]) > 2:
                return self.attendants[index.row()][2]
            return ""
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if 0 <= section < len(self.headers):
                    return self.headers[section]
                return ""
            else:
                return str(section)

    def insertRows(self, position, rows=1, index=QModelIndex()):
        """ Insert a row into the model. """
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)

        for row in range(rows):
            self.attendants.insert(position + row, ["name", "status", "Member"])
        
        self.endInsertRows()
        return True

    def removeRows(self, position, rows=1, index=QModelIndex()):
        """ Remove a row from the model. """
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        
        del self.attendants[position:position+rows]
        
        self.endRemoveRows()
        self.summaryChanged.emit()
        return True

    def setData(self, index, name, status, role="Member", editRole=Qt.EditRole):
        """ Adjust the data (set it to <value>) depending on the given 
            index and role. 
        """
        if editRole !=Qt.EditRole:
            return False

        if index.isValid() and 0 <= index.row() < len(self.attendants):
            attendant = self.attendants[index.row()]
            attendant[0] = name
            attendant[1] = status
            if len(attendant) > 2:
                attendant[2] = role
            else:
                attendant.append(role)            
            idx_end = self.index(index.row(), len(self.headers) - 1, QModelIndex())
            self.dataChanged.emit(index, idx_end)
            self.summaryChanged.emit()
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

    def updateStatus(self, name, status, role=None):
        """ Find the name in the array and use the index to update the status"""
        row = self.isExist(name)
        if not row == None:
            self.attendants[row][1] = status
            if role is not None:
                if len(self.attendants[row]) > 2:
                    self.attendants[row][2] = role
                else:
                    self.attendants[row].append(role)            
            idx_start = self.index(row, 0, QModelIndex())
            idx_end = self.index(row, len(self.headers) - 1, QModelIndex())
            if idx_start.isValid():
                self.dataChanged.emit(idx_start, idx_end)
            self.summaryChanged.emit()

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
        self.summaryChanged.emit()

    # Summary Statistics
    def get_member_signin_count(self):
        return sum(1 for a in self.attendants if len(a) > 2 and (a[2] or "").strip().lower() == "member" and a[1] == "SignIn")

    def get_member_signout_count(self):
        return sum(1 for a in self.attendants if len(a) > 2 and (a[2] or "").strip().lower() == "member" and a[1] == "SignOut")

    def get_member_total_count(self):
        return self.get_member_signin_count() + self.get_member_signout_count()

    def get_mentor_signin_count(self):
        return sum(1 for a in self.attendants if len(a) > 2 and (a[2] or "").strip().lower() in ["mentor", "memtor"] and a[1] == "SignIn")

    def get_mentor_signout_count(self):
        return sum(1 for a in self.attendants if len(a) > 2 and (a[2] or "").strip().lower() in ["mentor", "memtor"] and a[1] == "SignOut")

    def get_mentor_total_count(self):
        return self.get_mentor_signin_count() + self.get_mentor_signout_count()

    def get_total_signin_count(self):
        return sum(1 for a in self.attendants if a[1] == "SignIn")

    def get_total_signout_count(self):
        return sum(1 for a in self.attendants if a[1] == "SignOut")

    def get_grand_total_count(self):
        return len(self.attendants)

    memberSignInCount = Property(int, fget=get_member_signin_count, notify=summaryChanged)
    memberSignOutCount = Property(int, fget=get_member_signout_count, notify=summaryChanged)
    memberTotalCount = Property(int, fget=get_member_total_count, notify=summaryChanged)

    mentorSignInCount = Property(int, fget=get_mentor_signin_count, notify=summaryChanged)
    mentorSignOutCount = Property(int, fget=get_mentor_signout_count, notify=summaryChanged)
    mentorTotalCount = Property(int, fget=get_mentor_total_count, notify=summaryChanged)

    totalSignInCount = Property(int, fget=get_total_signin_count, notify=summaryChanged)
    totalSignOutCount = Property(int, fget=get_total_signout_count, notify=summaryChanged)
    grandTotalCount = Property(int, fget=get_grand_total_count, notify=summaryChanged)


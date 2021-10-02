# PySide2 Imports
from PySide2 import QtCore
from PySide2.QtCore import Signal, QObject

class AttnSignal(QObject):
    signal = Signal(str, str)
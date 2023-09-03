# PySide2 Imports
from PySide6 import QtCore
from PySide6.QtCore import Signal, QObject

class AttnSignal(QObject):
    signal = Signal(str, str)
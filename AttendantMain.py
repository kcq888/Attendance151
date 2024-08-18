from typing_extensions import Annotated

from PySide6 import QtCore
from Attendant import Attendant
import os, sys
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import QObject, QUrl, QCommandLineOption, QCommandLineParser
from PySide6.QtQml import qmlRegisterType
from AttendantModel import AttendantModel

def parse(app):
    """ parse the application arguments and options"""
    parser = QCommandLineParser()
    parser.addHelpOption()
    parser.addVersionOption()

    #Add command line options
    season_option = QCommandLineOption(
        "s",
        "Setting the FRC Season for the database, i.e., Season2024-2025.",
        "season"
    )
    parser.addOption(season_option)
    parser.process(app)
    return parser.value(season_option)

app = QGuiApplication(sys.argv)
app.setApplicationName("Attendance 151")
app.setApplicationVersion("5.0")

#Load the QML file
qml_file = os.path.join(os.path.dirname(__file__),"main.qml")
engine = QQmlApplicationEngine(parent=app)

qmlRegisterType(AttendantModel, "AttendantModel", 1, 0, "AttendantModel")

# create context object and table view model
season = parse(app)
attendant = Attendant(season)

# setting context objects to QML
context = engine.rootContext()
context.setContextProperty("attendantModel", attendant.attendantModel())
context.setContextProperty("attendant", attendant)

# loading qml
engine.load(QUrl.fromLocalFile(os.path.abspath(qml_file)))
mainWindow = engine.rootObjects()[0]
appAttend = mainWindow.findChild(QtCore.QObject, "attendant")
appAttend.dateChanged.connect(attendant.clearAttendants)
engine.quit.connect(app.quit)

#execute and cleanup
app.exec_()
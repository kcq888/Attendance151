from typing_extensions import Annotated
from Attendant import Attendant
import os, sys
from PySide2.QtQml import QQmlApplicationEngine
from PySide2.QtGui import QGuiApplication
from PySide2.QtCore import QObject, QUrl
from PySide2.QtQml import qmlRegisterType
from AttendantModel import AttendantModel

app = QGuiApplication(sys.argv)

#Load the QML file
qml_file = os.path.join(os.path.dirname(__file__),"main.qml")
engine = QQmlApplicationEngine(parent=app)

qmlRegisterType(AttendantModel, "AttendantModel", 1, 0, "AttendantModel")

# create context object and table view model
attendant = Attendant()

# setting context objects to QML
context = engine.rootContext()
context.setContextProperty("attendantModel", attendant.attendantModel())
context.setContextProperty("attendant", attendant)

# loading qml
engine.load(QUrl.fromLocalFile(os.path.abspath(qml_file)))
engine.quit.connect(app.quit)

#execute and cleanup
app.exec_()
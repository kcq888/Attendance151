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

engine.load(QUrl.fromLocalFile(os.path.abspath(qml_file)))
engine.quit.connect(app.quit)

attendantModel = AttendantModel()
context = engine.rootContext()
context.setContextProperty("attendantModel", attendantModel)

#execute and cleanup
app.exec_()
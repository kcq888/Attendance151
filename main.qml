import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    id: mainWindow
    visible: true
    visibility: Qt.WindowFullScreen
    width: 600
    height: 500
    title: "Touch Techs Attendant"

    AttendantView{}
}
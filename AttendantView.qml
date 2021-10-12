import QtQuick 2.6
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.1
import AttendantModel 1.0

 Item {
    id: appAttend
    width: parent.width
    height: parent.height
    objectName: "attendant"
    
    signal dateChanged()

    Rectangle {
        id: attendantBackground
        anchors.fill: parent
        gradient: Gradient {
            GradientStop {
                position: 0
                color: "#af9fc9"
            }

            GradientStop {
                position: 1
                color: "#5415b8"
            }
        }
    }

    GridLayout {
        id: appGrid
        
        anchors.fill: parent
        columns: 2
        rows: 1
        columnSpacing: 10
        
        Column {
            id: appContentLeft
            Layout.fillHeight: true
            Layout.column: 0
            Layout.row: 0
            Layout.columnSpan: 1
            Layout.minimumWidth: parent.width / 2
            Layout.maximumWidth: parent.width / 2
            Layout.alignment: Qt.AlignTop
            Layout.margins: 20
            
            Row {
                id: header
                Image {
                    id: image
                    width: 100
                    height: 100
                    fillMode: Image.Stretch
                    source: "./assets/images/2018_Logo.png"
                }
                Column {
                    Label {
                        color: "#dae3d9"
                        text: qsTr("Tough Techs 151 Attendant")
                        font.family: "Verdana"
                        font.bold: true
                        font.pointSize: 22
                        fontSizeMode: Text.HorizontalFit
                        renderType: Text.QtRendering
                        lineHeight: 1
                    }

                    Label {
                        id: currentDate
                        color: "#dae3d9"
                        text: ""
                        font.family: "Verdana"
                        font.bold: false
                        font.pointSize: 30
                        fontSizeMode: Text.HorizontalFit
                        renderType: Text.QtRendering
                        lineHeight: 1
                    }
                    Label {
                        id: currentTime
                        color: "#dae3d9"
                        text: ""
                        font.family: "Verdana"
                        font.bold: true
                        font.pointSize: 30
                        fontSizeMode: Text.HorizontalFit
                        renderType: Text.QtRendering
                        lineHeight: 1
                    }                
                }
            }
            TextField {
                id: rfidTextField
                placeholderText: qsTr("Scan Name Tag")
                focus: true
                onAccepted: {
                    //console.debug("RFID: ", rfidTextField.text)
                    attendant.onRfidAccepted(rfidTextField.text)
                    rfidTextField.text = ""
                }
            }
            Column {                
                Text {
                    id: nameText
                    font.family: "Verdana"
                    font.bold: true
                    font.pointSize: 24
                    color: "white"
                    text: attendant.name
                }
                Text {
                    id: statusText
                    font.family: "Verdana"
                    font.bold: true
                    font.pointSize: 24
                    color: "white"       
                    text: attendant.status     
                }
            }
        }
        Column {
            id: appContentRight
            width: parent.width / 2
            
            Layout.fillHeight: true
            Layout.column: 1
            Layout.row: 0
            Layout.columnSpan: 1
            Layout.minimumWidth: parent.width / 2
            Layout.alignment: Qt.AlignTop
            Layout.margins: 20
            
            Row {
                id: attendRow
                Label{
                    color: "#dae3d9"
                    text: qsTr("Today's Attendant")
                    font.family: "Verdana"
                    font.bold: true
                    font.pointSize: 22
                    fontSizeMode: Text.HorizontalFit
                    renderType: Text.QtRendering
                    lineHeight: 1
                }
            }
            TableView {
                id: statusTable
                width: parent.width - 80
                height: parent.height - attendRow.height

                model: attendantModel

                TableViewColumn {
                    id: nameColumn
                    role: "Name"
                    title: "Name"
                    width: parent.width / 4
                }
                TableViewColumn {
                    id: statusColumn
                    role: "Status"
                    title: "Status"
                    width: statusTable.width - nameColumn.width - 2
                }

                headerDelegate: Rectangle {
                    color: "#800080"
                    height: 25
                    Text {
                        text: styleData.value
                        color: "#FFF"
                        width: parent.width
                        height: parent.height
                        font.pointSize: 20
                        font.family: "Verdana"
                        minimumPointSize: 3
                        fontSizeMode: Text.Fit
                        font.bold: true
                        leftPadding: 5.0
                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
                    }
                }

                itemDelegate: Rectangle {
                    color: ["#f0ffff", "#d3d3d3"][styleData.row % 2]
                    height: 20
                    Text {
                        text: styleData.value
                        color: "#191970"
                        font.pointSize: 16
                        minimumPointSize: 3
                        fontSizeMode: Text.Fit
                        font.family: "Verdana"
                        leftPadding: 5.0
                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
                    }
                }

                Component.onCompleted: {
                    console.debug("parent height: ", parent.height)
                    console.debug("attend label height: ", attendRow.height)

                    var maxheight = appContentRight.height - attendRow.height - 40
                    console.debug("tableview max height:", maxheight)
                }
                
            }
        }
    }

    Timer {
        running: true
        triggeredOnStart: true
        repeat: true
        interval: 100

        onTriggered: {
            var date = new Date()
            currentTime.text = date.toTimeString().substring(0, 8)
            //interval = 1000 * (60 - date.getSeconds())

            currentDate.text = date.toLocaleDateString(Qt.locale(), "dddd MMMM d yyyy")
            if (date.getHours() === 0 && date.getMinutes() === 59)
                appAttend.dateChanged()
            restart()
        }
    }
}
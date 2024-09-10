import QtQuick 2.15
import QtQuick.Controls 2.15
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
            Item {
                height: 20
                width: parent.width
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
                    font.pointSize: 20
                    fontSizeMode: Text.HorizontalFit
                    renderType: Text.QtRendering
                    lineHeight: 1
                    height: 40
                    width: 200
                }
                TextField {
                    id: rfidTextField
                    Layout.leftMargin: 10
                    placeholderText: qsTr("Scan Name Tag")
                    focus: true
                    onAccepted: {
                        //console.debug("RFID: ", rfidTextField.text)
                        attendant.onRfidAccepted(rfidTextField.text)
                        rfidTextField.text = ""
                    }
                }
                 Text {
                    id: nameText
                    leftPadding: 10
                    font.family: "Verdana"
                    font.bold: true
                    font.pointSize: 20
                    color: "white"
                    text: attendant.name
                }
            }

            TableView {
                id: statusTable
                height: parent.height - attendRow.height
                width: parent.width
                columnWidthProvider: function (column) { return parent.width/2 - 40 }
                rowHeightProvider: function (column) { return 35; }
                topMargin: columnsHeader.implicitHeight
                ScrollBar.horizontal: ScrollBar{}
                ScrollBar.vertical: ScrollBar{}
                clip: true

                model: attendantModel

                delegate: Rectangle {
                    border.width: 1
                    border.color: "blue"
                    color: ["#f0ffff", "#d3d3d3"][styleData.row % 2]
                    Text {
                        text: display
                        anchors.fill: parent
                        anchors.margins: 10
                        color: "#191970"
                        fontSizeMode: Text.Fit
                        font.family: "Verdana"
                        font.pixelSize: 16
                        leftPadding: 5.0
                        horizontalAlignment: Text.AlignLeft
                        verticalAlignment: Text.AlignVCenter
                    }
                }
                Rectangle { // mask the headers
                    z: 3
                    color: "gray"
                    y: statusTable.contentY
                    x: statusTable.contentX
                    width: statusTable.leftMargin
                    height: statusTable.topMargin
                }

                Row {
                    id: columnsHeader
                    y: statusTable.contentY
                    z: 2
                    Repeater {
                        model: statusTable.columns > 0 ? statusTable.columns : 1
                        Label {
                            width: statusTable.columnWidthProvider(modelData)
                            height: 40
                            text: attendantModel.headerData(modelData, Qt.Horizontal)
                            color: 'white'
                            font.pixelSize: 15
                            font.bold: true
                            padding: 10
                            verticalAlignment: Text.AlignVCenter

                            background: Rectangle { color: "purple" }
                        }
                    }
                }
                ScrollIndicator.horizontal: ScrollIndicator { }
                ScrollIndicator.vertical: ScrollIndicator { }

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
            if (date.getHours() === 0 && date.getMinutes() === 0)
                appAttend.dateChanged()
            restart()
        }
    }
}
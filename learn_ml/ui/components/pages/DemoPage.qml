import QtQuick 2.0
import QtQuick.Window 2.0
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import Deploy 1.0

Page {
    id: root
    property alias openProjectButton: startButton

    anchors.fill:parent

    // Signals
    signal openProject(string sourceFile)

    signal reStreamChanged(string stream)

    Connections {
        target: root
        function onReStreamChanged(stream) { 

            if (videoButton.selected) {
                streamButton.visible = true
                streamButton.stream = stream 
            }        
        }
    }
    Component.onCompleted: deployManager.streamChanged.connect(reStreamChanged)


    DeployManager {
        id: deployManager
    }

    // background color for welcomePage
    Rectangle {
        id: pageBackground
        anchors.fill:parent
        color: "#131822"
        border.color: "#131822"

        // stacking logo ontop of button layout
        ColumnLayout{
            anchors.right: parent.right;   anchors.left: parent.left
            anchors.bottom: parent.bottom; anchors.top: parent.top

                // LearnML BigBrain Logo
                Image {
                    id: logo
                    height: 600
                    Layout.alignment: Qt.AlignHCenter
                    width: height * 1.25
                    x: parent.width/2 - width/2
                    y: parent.height/10
                    fillMode: Image.PreserveAspectFit
                    source: "../../graphics/Lml_Logo.png"

                    ParallelAnimation{
                        id: logoShrink
                        running: false

                        PropertyAnimation{ easing.type: Easing.InOutCubic;
                                           target: logo; property: "rotation"; to: logo.rotation + 360; duration: 1000;}
                        NumberAnimation { easing.type: Easing.InOutCubic;
                                          target: logo; property: "width"; to: 150; duration: 1000}
                        NumberAnimation { easing.type: Easing.InOutCubic;
                                          target: logo; property: "y"; to: -50; duration: 1000}

                    }

                }
            // WelcomePage Buttons Layout
            RowLayout {
                id: buttonLayout

                height: parent.height/4
                Layout.margins: 5
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignHCenter
                spacing: 50

                ColumnLayout {
                    id: taskColumn
                    height: parent.height
                    width: parent.width / 2
                    spacing: 50
                    

                    Text {
                        id: taskText
                        text: qsTr("Choose a Task")
                        font.pointSize: 18
                        color: "white"
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter

                    }

                    // Create Project Button
                    Button {
                        id: poseButton
                        text: qsTr("Pose Estimation")
                        property bool selected: false

                        onClicked: {
                            if (selected === false) {
                                selected = true
                                if (videoButton.selected || spiButton.selected) {
                                    startButton.visible = true
                                }
                            } 
                            if (faceButton.selected === true) {
                                faceButton.selected = false
                            }
                        }

                        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        Layout.preferredWidth: 300
                        Layout.preferredHeight: 100
                        contentItem: Text {
                                text: parent.text
                                font.pointSize: 12
                                color: parent.selected ? "white" : "#131822"
                                horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter
                            }

                        background: Rectangle{
                            border.color: parent.down ? "pink" : "#131822"
                            color: parent.selected ? "gray" : "white"
                            opacity: parent.down? 1:0.90
                            border.width: 1; radius:parent.height
                        }
                    }

                    Button {
                        id: faceButton
                        text: qsTr("Face Detection")
                        property bool selected: false

                        onClicked: {
                            if (selected === false) {
                                selected = true
                                if (videoButton.selected || spiButton.selected) {
                                    startButton.visible = true
                                }
                            }
                            if (poseButton.selected === true) {
                                poseButton.selected = false
                            }
                         }

                        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        Layout.preferredWidth: 300
                        Layout.preferredHeight: 100
                        contentItem: Text {
                                text: parent.text
                                font.pointSize: 12
                                color: parent.selected ? "white" : "#131822"
                                horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter
                        }

                        background: Rectangle{
                            border.color: parent.down ? "pink" : "#131822"
                            color: parent.selected ? "gray" : "white"
                            opacity: parent.down? 1:0.90
                            border.width: 1; radius:parent.height
                        }
                    }
                }

                ColumnLayout {
                    id: streamColumn
                    height: parent.height
                    width: parent.width / 2
                    spacing: 50

                    Text {
                        id: streamText
                        text: qsTr("Choose a Stream")
                        font.pointSize: 18
                        color: "white"
                        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter

                    }

                    Button {
                        id: videoButton
                        text: qsTr("Video")
                        property bool selected: false
                        onClicked: {
                            if (selected === false) {
                                selected = true
                                if (faceButton.selected || poseButton.selected) {
                                    startButton.visible = true
                                }
                            } 
                            if (spiButton.selected === true) {
                                spiButton.selected = false
                            }
                        }

                        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        Layout.preferredWidth: 300
                        Layout.preferredHeight: 100
                        contentItem: Text {
                                text: parent.text
                                font.pointSize: 12
                                color: parent.selected ? "white" : "#131822"
                                horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter
                        }

                        background: Rectangle{
                            border.color: parent.down ? "pink" : "#131822"
                            color: parent.selected ? "gray" : "white"
                            opacity: parent.down? 1:0.90
                            border.width: 1; radius:parent.height
                        }
                    }

                    Button {
                        id: spiButton
                        text: qsTr("Arduino")
                        property bool selected: false
                        onClicked: {
                            if (selected === false) {
                                selected = true
                                if (faceButton.selected || poseButton.selected) {
                                    startButton.visible = true
                                }
                            } 
                            if (videoButton.selected === true) {
                                videoButton.selected = false
                            }
                        }

                        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        Layout.preferredWidth: 300
                        Layout.preferredHeight: 100
                        contentItem: Text {
                            text: parent.text
                            font.pointSize: 12
                            color: parent.selected ? "white" : "#131822"
                            horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter
                        }

                        background: Rectangle{
                            border.color: parent.down ? "pink" : "#131822"
                            color: parent.selected ? "gray" : "white"
                            opacity: parent.down? 1:0.90
                            border.width: 1; radius:parent.height
                        }
                    }
                }

                // Open Project Button    TODO: replace onClicked functionality with file explorer
                Button {
                    id: startButton
                    property bool selected: false
                    visible: false
                    onClicked: {
                        logoShrink.start()
                        selected = true

                        let task = ""
                        let stream = ""
                        if (poseButton.selected) {
                            task = "posenet"
                        }
                        else if (faceButton.selected) {
                            task = "face"
                        }

                        if (videoButton.selected) {
                            stream = "video"
                        }
                        else if (spiButton.selected) {
                            stream = "spi"
                        }

                        deployManager.deploy(task, stream)
                    }


                    // Button Styling --------------------------------
                    text: qsTr("Start")
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    Layout.preferredWidth: 300
                    Layout.preferredHeight: 100

                    contentItem: Text {
                            text: parent.selected ? "Started!" : parent.text
                            font.pointSize: 12
                            color: parent.selected ? "white" : "#131822"
                            horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter
                        }

                    background: Rectangle{
                        border.color: parent.down ? "pink" : "#131822"
                        color: parent.selected ? "gray" : "white"
                        opacity: parent.down? 1:0.90
                        border.width: 1; radius:parent.height
                    }
                }

            }
        }
        Button {
            id: streamButton
            x: parent.width / 2 - width / 2
            y: parent.height / 2 - height / 2
            visible: false

            width: 350
            height: 100

            property string stream: "..."

            // Button Styling --------------------------------
            text: qsTr("Stream accessible at " + stream)

            contentItem: Text {
                    text: parent.text
                    font.pointSize: 12
                    color: parent.selected ? "white" : "#131822"
                    horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter
                }

            background: Rectangle{
                border.color: parent.down ? "pink" : "#131822"
                color: parent.selected ? "gray" : "white"
                opacity: parent.down? 1:0.90
                border.width: 1; radius:parent.height
            }
        }

        Button {
            id: resetButton

            width: 100
            height: 50

            anchors.right: parent.right
            anchors.rightMargin: 25
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 25
            onClicked: {
                poseButton.selected = false 
                faceButton.selected = false 
                videoButton.selected = false 
                spiButton.selected = false 
                startButton.selected = false
                streamButton.visible = false
                streamButton.stream = "..."
            }

            // Button Styling --------------------------------
            text: qsTr("Reset")

            contentItem: Text {
                    text: parent.text
                    font.pointSize: 12
                    color: parent.selected ? "white" : "#131822"
                    horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter
                }

            background: Rectangle{
                border.color: parent.down ? "pink" : "#131822"
                color: parent.selected ? "gray" : "white"
                opacity: parent.down? 1:0.90
                border.width: 1; radius:parent.height
            }
        }
    }
}

/*##^##
Designer {
    D{i:0;autoSize:true;formeditorZoom:0.33000001311302185;height:480;width:640}
}
##^##*/

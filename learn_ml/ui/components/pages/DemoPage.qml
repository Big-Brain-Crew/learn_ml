import QtQuick 2.0
import QtQuick.Window 2.0
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15

Page {
    id: root
    property alias openProjectButton: proj5Button

    anchors.fill:parent

    // Signals
    signal openProject(string sourceFile)

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

                // Create Project Button
                Button {
                    id: proj1Button
                    text: qsTr("Project 1")
//                  onClicked: create a project file and stuff ------------- TODO

                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    Layout.preferredWidth: 300
                    Layout.preferredHeight: 100
                    contentItem: Text {
                            text: parent.text
                            font.pointSize: 12
                            color: parent.down ? "green" : "#131822"
                            horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter
                        }

                    background: Rectangle{
                        border.color: parent.down ? "green" : "#131822"
                        opacity: parent.down? 1:0.90
                        border.width: 1; radius:parent.height
                    }
                }

                Button {
                    id: proj2Button
                    text: qsTr("Project 2")
//                  onClicked: create a project file and stuff ------------- TODO

                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    Layout.preferredWidth: 300
                    Layout.preferredHeight: 100
                    contentItem: Text {
                            text: parent.text
                            font.pointSize: 12
                            color: parent.down ? "green" : "#131822"
                            horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter
                        }

                    background: Rectangle{
                        border.color: parent.down ? "green" : "#131822"
                        opacity: parent.down? 1:0.90
                        border.width: 1; radius:parent.height
                    }
                }

                Button {
                    id: proj3Button
                    text: qsTr("Project 3")
//                  onClicked: create a project file and stuff ------------- TODO

                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    Layout.preferredWidth: 300
                    Layout.preferredHeight: 100
                    contentItem: Text {
                            text: parent.text
                            font.pointSize: 12
                            color: parent.down ? "green" : "#131822"
                            horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter
                        }

                    background: Rectangle{
                        border.color: parent.down ? "green" : "#131822"
                        opacity: parent.down? 1:0.90
                        border.width: 1; radius:parent.height
                    }
                }

                Button {
                    id: proj4Button
                    text: qsTr("Project 4")
//                  onClicked: create a project file and stuff ------------- TODO

                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    Layout.preferredWidth: 300
                    Layout.preferredHeight: 100
                    contentItem: Text {
                            text: parent.text
                            font.pointSize: 12
                            color: parent.down ? "green" : "#131822"
                            horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter
                        }

                    background: Rectangle{
                        border.color: parent.down ? "green" : "#131822"
                        opacity: parent.down? 1:0.90
                        border.width: 1; radius:parent.height
                    }
                }

                // Open Project Button    TODO: replace onClicked functionality with file explorer
                Button {
                    id: proj5Button
                    onClicked: logoShrink.start()
                    //onClicked: root.openProject("components/pages/WorkspacePage.qml")


                    // Button Styling --------------------------------
                    text: qsTr("Project 5")
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                    Layout.preferredWidth: 300
                    Layout.preferredHeight: 100

                    contentItem: Text {
                            text: openProjectButton.text;  font.pointSize: 12
                            color: openProjectButton.down ? "green" : "#131822"
                            horizontalAlignment: Text.AlignHCenter;  verticalAlignment: Text.AlignVCenter
                        }

                    background: Rectangle{
                        border.color: openProjectButton.down ? "green" : "#131822"
                        opacity: openProjectButton.down? 1:0.90
                        border.width: 1;   radius:parent.height
                    }

                }

            }
        }

    }

}

/*##^##
Designer {
    D{i:0;autoSize:true;formeditorZoom:0.33000001311302185;height:480;width:640}
}
##^##*/

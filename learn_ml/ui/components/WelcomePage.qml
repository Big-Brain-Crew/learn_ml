import QtQuick 2.0
import QtQuick.Window 2.0
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15

    Page {
        id: welcomePage
        anchors.fill:parent

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
                        height: 500
                        Layout.alignment: Qt.AlignHCenter
                        width: height * 1.25
                        x: parent.width/2 - width/2
                        y: parent.height/10
                        fillMode: Image.PreserveAspectFit
                        source: "../graphics/Lml_Logo.png"

                    }
                // WelcomePage Buttons Layout
                RowLayout {
                    id: buttonLayout

                    height: parent.height/4
                    Layout.margins: 5
                    Layout.fillWidth: true
                    Layout.alignment: Qt.AlignHCenter
                    spacing: 150

                    // Create Project Button
                    Button {
                        id: createProjectButton
                        text: qsTr("Create Project")
//                        onClicked: appAction.CreateProject()        TODO

                        Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                        Layout.preferredWidth: 300
                        Layout.preferredHeight: 100
                        contentItem: Text {
                                text: createProjectButton.text
                                font.pointSize: 12
                                color: createProjectButton.down ? "green" : "#131822"
                                horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter
                            }

                        background: Rectangle{
                            border.color: createProjectButton.down ? "green" : "#131822"
                            opacity: createProjectButton.down? 1:0.90
                            border.width: 1; radius:parent.height
                        }
                    }

                    // Open Project Button
                    Button {
                        id: openProjectButton
                        text: qsTr("Open Project")
//                        onClicked: appAction.OpenProject()        TODO

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

import QtQuick 2.0
import QtQuick.Layouts 1.15
import QtQuick.Controls 1.4

Item {
    id: root

    // Resizable view
    SplitView{
        id: layoutGuy
        anchors.fill:parent
        orientation: Qt.Horizontal

        // PLACEHOLDER for Train Editor -
        Rectangle{
            id: editorPanelTrain
            Layout.minimumWidth: 900
            Layout.fillHeight: true
            Layout.fillWidth: true
            // ladies blue
            color: "#1ad1e5"

            // for labeling which page is loaded
            Text {
                anchors.fill:parent
                id: whatItIs
                text: qsTr("I'm the Train Editor Panel!")
                font.family: "Helvetica"; font.pointSize: 25; font.bold: true
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
        }
    }
}

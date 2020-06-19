import QtQuick 2.0
import QtQuick.Layouts 1.15
import QtQuick.Controls 1.4

Item {
    id: root

    // Resizable View
    SplitView{
        id: splitView
        anchors.fill:parent
        orientation: Qt.Horizontal

        // PLACEHOLDER for Deploy Editor -
        Rectangle{
            id: editorPanelDeploy
            Layout.minimumWidth: 900
            Layout.fillHeight: true
            Layout.fillWidth: true
            // boobie red
            color: "#b00b1e"

            // for labeling which page is loaded -
            Text {
                anchors.fill:parent
                id: whatItIs
                text: qsTr("I'm the Deploy Editor Panel!")
                font.family: "Helvetica"; font.pointSize: 25; font.bold: true
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
        }
    }
}

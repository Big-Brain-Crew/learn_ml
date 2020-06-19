import QtQuick 2.0
import QtQuick.Layouts 1.15
import QtQuick.Controls 1.4

Item {
    id: root

    // Resizable View
    SplitView{
        id: layoutGuy
        anchors.fill:parent
        orientation: Qt.Horizontal

        // PLACEHOLDER for Model Searchpanel -
        Rectangle{
            id: searchPanelModel
            width:350
            Layout.minimumWidth: 100
            Layout.fillHeight:true
            // this is a bad cad color
            color: "#b1ade5"
        }

        // PLACEHOLDER for Model Editor -
        Rectangle{
            id: editorPanelModel
            Layout.minimumWidth: 900
            Layout.fillHeight: true
            Layout.fillWidth: true
            // 2 for 1 dates!
            color: "#241d85"

            // for labeling which page is loaded
            Text {
                anchors.fill:parent
                id: whatItIs
                text: qsTr("I'm the Model Editor Panel!")
                font.family: "Helvetica"; font.pointSize: 25; font.bold: true
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
        }
    }
}

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


        // PLACEHOLDER for Dataset SearchPanel -
        Rectangle{
            id: searchPanelDataset
            width:350
            Layout.minimumWidth: 100
            Layout.fillHeight:true
            // helloo upside down color
            color: "#431100"
        }

        // PLACEHOLDER for Dataset Editor -
        Rectangle{
            id: editorPanelDataset
            Layout.minimumWidth: 900
            Layout.fillHeight: true
            Layout.fillWidth: true
            // doobie red
            color: "#d00b13"

            // for labeling which page is loaded
            Text {
                anchors.fill:parent
                id: whatItIs
                text: qsTr("I'm the Dataset Editor Panel!")
                font.family: "Helvetica"; font.pointSize: 25; font.bold: true
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
        }
    }
}

/*##^##
Designer {
    D{i:0;autoSize:true;height:480;width:640}
}
##^##*/

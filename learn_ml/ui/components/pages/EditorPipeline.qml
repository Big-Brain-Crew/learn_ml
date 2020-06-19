import QtQuick 2.0
import QtQuick.Layouts 1.15
import QtQuick.Controls 1.4

Item {
    id: root

    SplitView{
        id: layoutGuy
        anchors.fill:parent
        orientation: Qt.Horizontal

        // PLACEHOLDER for Pipeline SearchPanel -
        Rectangle{
            id: searchPanelPipeline
            width:350
            Layout.minimumWidth: 100
            Layout.fillHeight:true
            // feeels yellow
            color: "#feee15"
        }

        // PLACEHOLDER for Pipeline Editor -
        Rectangle{
            id: editorPanelPipeline
            Layout.minimumWidth: 900
            Layout.fillHeight: true
            Layout.fillWidth: true
            // feable orange
            color: "#feab13"

            // for labeling which page is loaded
            Text {
                anchors.fill:parent
                id: whatItIsText
                text: qsTr("I'm the Pipeline Editor Panel!")
                font.family: "Helvetica"; font.pointSize: 25; font.bold: true
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
        }
    }
}

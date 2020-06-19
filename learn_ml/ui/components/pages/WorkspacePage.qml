import QtQuick 2.0
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15

Item {
    id: root

    //Stack the navigation panel with on top of the editor panels
    ColumnLayout{
        anchors.fill: parent

        // PLACEHOLDER navigation bar
        Slider{
            id: navSlider
            height: 100

            Layout.fillWidth: true
            Layout.alignment: Qt.AlignHCenter

            stepSize: 1
            snapMode: Slider.SnapOnRelease
            value: 1
            from: 1
            to: 5
        }

        // Editor Loader
        Loader{
            id: editorLoader
            Layout.fillHeight: true
            Layout.fillWidth: true

            source: {
                switch (navSlider.value){
                    case 1 : return "EditorDataset.qml"
                    case 2 : return "EditorPipeline.qml"
                    case 3 : return "EditorModel.qml"
                    case 4 : return "EditorTrain.qml"
                    case 5 : return "EditorDeploy.qml"
                }
            }
        }
    }

}

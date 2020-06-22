import QtQuick 2.12
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import ".."

Rectangle {
    id: root
    anchors.fill: parent

    /// Public Interface ///
    
    /* Define with object creation */
    required property var modelEditorPageModel

    /// End Public Interface

    readonly property var dispatcher: modelEditorPageModel.dispatcher

    FocusScope {
        anchors.fill: parent
        focus: true

        RowLayout {
            anchors.fill: parent
            spacing: 0

            NodeSearchPanelView {
                id: nodeSearchPanelView             
                Layout.fillHeight: true
                Layout.preferredWidth: 480
                Layout.preferredHeight: 1080
                focus: true

                nodeSearchPanelModel: root.modelEditorPageModel.nodeSearchPanelModel
            }

            ColumnLayout {
                spacing: 0

                NavigationBarView {
                    id: navigationBarView 
                    Layout.preferredHeight: 200
                    Layout.alignment: Qt.AlignHCenter

                    navigationBarModel: root.modelEditorPageModel.navigationBarModel
                }

                NodeCanvasView {
                    id: nodeCanvasView
                    Layout.preferredHeight: 880
                    Layout.fillHeight: true

                    nodeCanvasModel: root.modelEditorPageModel.nodeCanvasModel
                }
            }
        }
    }

}
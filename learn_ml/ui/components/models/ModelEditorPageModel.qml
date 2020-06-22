import QtQuick 2.12
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    id: root

    /// Public Interface ///

    /* Define with object creation */
    property alias dispatcher: logicConnection.target

    /* Properties */
    readonly property alias navigationBarModel: navigationBarModel
    readonly property alias nodeSearchPanelModel: nodeSearchPanelModel
    readonly property alias nodeCanvasModel: nodeCanvasModel 

    /// End Public Interface ///

    NavigationBarModel {
        id: navigationBarModel
        dispatcher: modelEditorPageLogic.navigationBarLogic
    }

    NodeSearchPanelModel {
        id: nodeSearchPanelModel 
        dispatcher: modelEditorPageLogic.nodeSearchPanelLogic
    }

    NodeCanvasModel {
        id: nodeCanvasModel
        dispatcher: modelEditorPageLogic.nodeCanvasLogic
    }

    Connections {
        id: logicConnection
    }

}

import QtQuick 2.12

Item {
    id: root

    /// Public Interface ///

    /* Properties */
    readonly property alias navigationBarLogic: navigationBarLogic
    readonly property alias nodeSearchPanelLogic: nodeSearchPanelLogic
    readonly property alias nodeCanvasLogic: nodeCanvasLogic

    /* Signals */

    /// End Public Interface ///

    NavigationBarLogic {
        id: navigationBarLogic
    }

    NodeSearchPanelLogic {
        id: nodeSearchPanelLogic
    }

    NodeCanvasLogic {
        id: nodeCanvasLogic
    }

    Connections {
        id: navigationBarLogicConnection
        target: navigationBarLogic

        function onDatasetButtonPressed() {
            console.log("Switching to dataset page")
        }
        function onPipelineButtonPressed() {
            console.log("Switching to pipeline page")
        }
        function onModelButtonPressed() {
            console.log("Switching to model page")
        }
        function onTrainButtonPressed() {
            console.log("Switching to train page")
        }
        function onDeployButtonPressed() {
            console.log("Switching to deploy page")
        }
    }

    Connections {
        id: nodeBarLogicConnection
        target: nodeSearchPanelLogic

        function onSelectNode(name) {
            nodeCanvasLogic.createNode(name)
        }
    }

    Connections {
        id: nodeCanvasLogicConnection
        target: nodeCanvasLogic
    }
}
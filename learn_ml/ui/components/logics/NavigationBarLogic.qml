import QtQuick 2.12

Item {
    id: root

    /// Public Interface ///

    /* Properties */
    readonly property alias datasetButtonLogic: datasetButtonLogic
    readonly property alias pipelineButtonLogic: pipelineButtonLogic
    readonly property alias modelButtonLogic: modelButtonLogic
    readonly property alias trainButtonLogic: trainButtonLogic
    readonly property alias deployButtonLogic: deployButtonLogic

    /* Signals */
    signal datasetButtonPressed()
    signal pipelineButtonPressed()
    signal modelButtonPressed()
    signal trainButtonPressed()
    signal deployButtonPressed()

    /// End Public Interface ///

    CircleButtonLogic {
        id: datasetButtonLogic
    }

    CircleButtonLogic {
        id: pipelineButtonLogic
    }

    CircleButtonLogic {
        id: modelButtonLogic
    }

    CircleButtonLogic {
        id: trainButtonLogic
    }

    CircleButtonLogic {
        id: deployButtonLogic
    }

    Connections {
        id: datasetButtonLogicConnection
        target: root.datasetButtonLogic

        function onButtonPressed(text) {
            root.datasetButtonPressed()
        }
    }

    Connections {
        id: pipelineButtonLogicConnection
        target: pipelineButtonLogic

        function onButtonPressed(text) {
            root.pipelineButtonPressed()
        }
    }

    Connections {
        id: modelButtonLogicConnection
        target: modelButtonLogic

        function onButtonPressed(text) {
            root.modelButtonPressed()
        }
    }

    Connections {
        id: trainButtonLogicConnection
        target: trainButtonLogic

        function onButtonPressed(text) {
            root.trainButtonPressed()
        }
    }

    Connections {
        id: deployButtonLogicConnection
        target: deployButtonLogic

        function onButtonPressed(text) {
            root.deployButtonPressed()
        }
    }
}
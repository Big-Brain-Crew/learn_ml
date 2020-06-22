import QtQuick 2.12
import "../logics"

Item {
    id: root

    /// Public Interface ///

    /* Define with object creation */
    property alias dispatcher: logicConnection.target

    /* Properties */
    readonly property alias datasetText: _.datasetText
    readonly property alias pipelineText: _.pipelineText
    readonly property alias modelText: _.modelText
    readonly property alias trainText: _.trainText
    readonly property alias deployText: _.deployText

    readonly property alias datasetButtonModel: datasetButtonModel
    readonly property alias pipelineButtonModel: pipelineButtonModel
    readonly property alias modelButtonModel: modelButtonModel
    readonly property alias trainButtonModel: trainButtonModel
    readonly property alias deployButtonModel: deployButtonModel

    /// End Public Interface ///

    // Private Properties
    Item {
        id: _
        property string datasetText: "Dataset"
        property string pipelineText: "Pipeline"
        property string modelText: "Model"
        property string trainText: "Train"
        property string deployText: "Deploy"
    }

    CircleButtonModel {
        id: datasetButtonModel
        dispatcher: root.dispatcher.datasetButtonLogic
        text: "Dataset"
    }

    CircleButtonModel {
        id: pipelineButtonModel
        dispatcher: root.dispatcher.pipelineButtonLogic
        text: "Pipeline"
    }

    CircleButtonModel {
        id: modelButtonModel
        dispatcher: root.dispatcher.modelButtonLogic
        text: "Model"
    }

    CircleButtonModel {
        id: trainButtonModel
        dispatcher: root.dispatcher.trainButtonLogic
        text: "Train"
    }

    CircleButtonModel {
        id: deployButtonModel
        dispatcher: root.dispatcher.deployButtonLogic
        text: "Deploy"
    }

    Connections {
        id: logicConnection
    }

}
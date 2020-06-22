import QtQuick 2.12

Rectangle {
    id: root

    /// Public Interface ///

    /* Define with object creation */
    // Connect to the NavigationBarModel
    required property var navigationBarModel

    /// End Public Interface

    readonly property var dispatcher: navigationBarModel.dispatcher

    Row {
        spacing: 50
        anchors.centerIn: parent

        CircleButtonView {
            id: datasetButtonView
            circleButtonModel: navigationBarModel.datasetButtonModel
        }

        CircleButtonView {
            id: pipelineButtonView
            circleButtonModel: navigationBarModel.pipelineButtonModel
        }

        CircleButtonView {
            id: modelButtonView
            circleButtonModel: navigationBarModel.modelButtonModel
        }

        CircleButtonView {
            id: trainButtonView
            circleButtonModel: navigationBarModel.trainButtonModel
        }

        CircleButtonView {
            id: deployButtonView
            circleButtonModel: navigationBarModel.deployButtonModel
        }
    }
}

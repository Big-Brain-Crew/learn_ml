import QtQuick 2.12
import "../models"

Rectangle {
    id: root
    color: "#102027"
    width: 1440
    height: 1080

    /// Public interface ///

    /* Define with object creation*/
    // Connect to the NodeCanvasModel
    required property var nodeCanvasModel

    /// End Public Interface ///

    /* Properties */
    property var nodeModelList: nodeCanvasModel.nodeModelList
    property var nodeViewList: []
    property int spacing: 25
    readonly property var dispatcher: nodeCanvasModel.dispatcher

    FocusScope {
        id: canvasScope
        width: parent.width
        height: parent.height
        focus: true

        // Temporary test button
        Rectangle {
            id: testButton
            width: 50
            height: 50
            color: "black"
            anchors.right: parent.right
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    dispatcher.createNode("Dense")
                }
            }
        }
        
        // Temporary training button
        Rectangle {
            id: trainButton
            width: 50
            height: 50
            color: "blue"
            anchors.right: parent.right
            anchors.top: testButton.bottom
            MouseArea {
                anchors.fill: parent
                onClicked: {
                    dispatcher.train()
                }
            }
        }
    }

    /* Connections */

    // Listens to the NodeCanvasModel
    Connections {
        id: nodeCanvasModelConnection
        target: nodeCanvasModel

        function onNodeCreated(name) {
            root.createNodeView(name)
        }
    }

    /* Functions */

    // Create a new NodeView
    function createNodeView(name) {
        var nodeViewComponent = Qt.createComponent("NodeView.qml")
        let nodeModel = nodeModelList[nodeModelList.length - 1]

        let coords = root.newNodeCoords()

        let instance = nodeViewComponent.createObject(root,
            {name: name, nodeModel: nodeModel, 
            x: coords[0], y: coords[1]})

        nodeViewList.push(instance)
    }

    // Define coordinates for a new NodeView based off existing 
    // nodeView coordinates
    function newNodeCoords() {
        let x = 0; let y = 0
        if (nodeViewList.length == 0){
            x = 600
            y = root.height / 2
        }
        else {
            let nodeView = nodeViewList[nodeViewList.length - 1]
            x = nodeView.x + nodeView.width + spacing
            y = nodeView.y
        }
        return [x, y]
    }
}




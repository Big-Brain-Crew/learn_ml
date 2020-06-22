import QtQuick 2.12
import Node 1.0
import "../"

Item {
    id: root

    /// Public interface ///

    /* Define with object creation */
    // Connect to the Logic component
    property alias dispatcher: logicConnection.target

    /* Properties */
    readonly property alias nodeModelList: _.nodeModelList
    
    // Emitted when a new nodeModel is created. The nodeCanvasView should 
    // subscribe to this signal.
    signal nodeCreated(string name)

    /// End Public Interface ///

    // Private properties
    Item {
        id: _ 
        property var nodeModelList: [] // Store dynamically created nodeModels
        property string nodeFilePath: "NodeModel.qml"
    }

    // Node Manager API
    NodeManager{
        id: nodeManager
    }

    /* Connections */
    Connections {
        id: logicConnection
        
        function onCreateNodeModel(name, coords) {
            root.createNodeModel(name, coords)
        }

        function onTrain() {
            root.train()
        }
    }

    /* Functions */

    // Create a new NodeModel
    function createNodeModel(name) {
        // Retrieve parameters from the backend
        var parameters = nodeManager.get_parameters(name)

        // Create the node
        var nodeComponent = Qt.createComponent(_.nodeFilePath)
        
        let identifier = name + _.nodeModelList.length
        let nodeLogicList = root.dispatcher.nodeLogicList

        // Each node component has its own logic
        let dispatcher = nodeLogicList[nodeLogicList.length - 1]

        // Instantiate the node
        let instance = nodeComponent.createObject(root, 
            {name: name, identifier: identifier,
            parameters: parameters, dispatcher: dispatcher})

        // Add the node to list and to the backend
        _.nodeModelList.push(instance)
        nodeManager.add_node(name)

        // Notify the view it has another nodeModel to display
        root.nodeCreated(name)
    }

    // Update the backend node manager and begin training
    function train() {
        nodeManager.update_params(_.nodeModelList)
        nodeManager.train()
    }
   
}
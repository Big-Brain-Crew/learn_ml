import QtQuick 2.12

Item {
    id: root

    /// Public Interface ///

    readonly property alias nodeLogicList: _.nodeLogicList

    /*Signals */
    signal createNodeModel(string name)
    signal train()

    /* Functions */
    function createNode(name) {
        createNodeImpl(name)
    }

    /// End Public Interface

    readonly property string nodeLogicFilePath: "NodeLogic.qml"

    Item {
        id: _
        property var nodeLogicList: []
    }

    function createNodeImpl(name) {

        // Create the node logic component
        var nodeLogicComponent = Qt.createComponent(root.nodeLogicFilePath)

        let logicId = "nodeLogic" + _.nodeLogicList.length

        // Instantiate the component
        let instance = nodeLogicComponent.createObject(root,
            {id: logicId})

        // Add to the logic list
        _.nodeLogicList.push(instance)

        root.createNodeModel(name)
    }
}
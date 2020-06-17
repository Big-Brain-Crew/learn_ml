import QtQuick 2.12
import Node 1.0

Rectangle {
    id: root
    color: "#102027"
    width: 1920
    height: 1080

    FocusScope {
        id: canvasScope
        width: parent.width
        height: parent.height
        focus: true

        NodeBar {
            id: nodeBar
            anchors.left: parent.left
            onNodeClicked: { nodeSpawner.createNode(name) }
            focus: true
        }

        // Temporary button
        Rectangle {
            id: button
            anchors.right: parent.right
            width: 50
            height: 50

            MouseArea {
                id: testMouseArea
                anchors.fill: parent
                onClicked: nodeSpawner.createNode("flatten")
            }
        }

        // Temporary
        Rectangle {
            id: trainButton
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.topMargin: 100
            width: 50
            height: 50
            color: "#37474f"

            Text {
                id: trainText
                text: "Train"
                color: "#000000"
                font.pointSize: 12
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter
                anchors.fill: parent
            }

            MouseArea {
                id: trainMouseArea
                anchors.fill: parent
                onClicked: nodeSpawner.train()
            }
        }

        // Custom object
        NodeManager{
            id: nodeManager
        }

        Item {
            id: nodeSpawner
            property var instances: []
            property int spacing: 25

            function createNode(name) {
                var parameters = nodeManager.get_parameters(name)
                var nodeComponent = Qt.createComponent("Node.qml")
                
                // parameters["value"] = null

                // Calculate x and y coordinates
                var x = 0; var y = 0
                if (instances.length == 0){
                    x = 600
                    y = root.height / 2
                }
                else {
                    x = instances[instances.length - 1].x +
                            instances[instances.length - 1].width + spacing
                    y = instances[instances.length - 1].y
                }

                let instance = nodeComponent.createObject(nodeSpawner, 
                    {x: x, y: y, text: name, parameters: parameters})
                instances.push(instance)
                nodeManager.add_node(name)
            }

            function train() {
                nodeManager.update_params(instances)
                nodeManager.train()
            }
        }
    }
}




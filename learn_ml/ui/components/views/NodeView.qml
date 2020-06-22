import QtQuick 2.12
import QtQuick.Controls 2.15

FocusScope {
    id: scope 
    width: root.width
    height: root.height 

    property alias name: nodeText.text
    property alias nodeModel: root.nodeModel

    Rectangle {
        id: root
        color: "#37474f"
        width: 75
        height: 75
        state: "initialState"

        /// Public Interface ///

        /* Define with object creation */

        // Connect to NodeModel
        required property var nodeModel

        /// End Public Interface ///

        readonly property var dispatcher: nodeModel.dispatcher

        Component.onCompleted: {
            parametersListView.model = root.nodeModel.parametersListModel
        }

        property int parameterHeight: 40
        property int parameterWidth: 150
        property int leftPadding: 20
        property int rightPadding: 20
        property int bottomPadding: 20

        Drag.active: dragArea.drag.active

        Text {
            id: nodeText
            text: nodeModel.name
            anchors.top: parent.top
            anchors.topMargin: 15
            anchors.horizontalCenter: parent.horizontalCenter
            color: "#ffffff"
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            font.pixelSize: 12
            height: 10
        }

        Rectangle {
            id: expandButton
            width: 15
            height: 15
            z: 1
            color: "#62727b"
            anchors.top: parent.top
            anchors.right: parent.right

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    if (root.state == "initialState"){
                        root.state = "expandedState"
                        scope.focus = true
                    } else if (root.state == "expandedState") {
                        root.state = "initialState"
                    }
                }
            }
        }
    
        MouseArea {
            id: dragArea
            anchors.fill: parent
            drag.target: parent
            onClicked: {
                scope.focus = true
            }
        }

        Component {
            id: parametersDelegate

            FocusScope {
                id: parametersDelegateScope
                width: parametersRect.width
                height: parametersRect.height
                property alias color: parametersRect.color
                property alias text: parameterTextInput.text
                focus: true

                Rectangle {
                    id: parametersRect
                    color: "#62727b"
                    width: root.parameterWidth
                    height: root.parameterHeight

                    Text {
                        id: parameterText
                        width: parent.width / 2
                        height: parent.height
                        anchors.left: parent.left
                        anchors.verticalCenter: parent.verticalCenter
                        verticalAlignment: Text.AlignVCenter
                        horizontalAlignment: Text.AlignHCenter
                        font.pixelSize: 12
                        color: "#ffffff"

                        // From Model
                        text: parameterName

                    }

                    TextInput {
                        id: parameterTextInput
                        width: parent.width / 2
                        height: parent.height
                        anchors.right: parent.right
                        anchors.verticalCenter: parent.verticalCenter
                        verticalAlignment: Text.AlignVCenter
                        horizontalAlignment: Text.AlignHCenter
                        font.pixelSize: 12
                        color: "#ffffff"
                        focus: true

                        // From Model
                        text: parameterValue

                        Keys.onReturnPressed: {
                            root.dispatcher.updateNodeParameterValue(
                                root.nodeModel.identifier, parameterText.text, text)
                        }
                    }
                }
            }
        }

        ListView {
            id: parametersListView
            width: root.parameterWidth
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: nodeText.bottom
            anchors.topMargin: 10
            anchors.bottom: parent.bottom
            clip: true
            visible: false
            focus: true
            keyNavigationWraps: true

            delegate: parametersDelegate

            Keys.onTabPressed: { incrementCurrentIndex() }
            Keys.onBacktabPressed: { decrementCurrentIndex() }
        }

        states: [
            State {
                name: "initialState"
            },
            State {
                name: "expandedState"
                PropertyChanges {
                    target: root
                    height: parametersListView.count * root.parameterHeight + nodeText.height +
                            nodeText.anchors.topMargin + bottomPadding
                    width: root.parameterWidth + leftPadding + rightPadding
                    border.color: "#ff4081"
                }
                PropertyChanges {
                    target: parametersListView
                    visible: true
                }
            }

        ]
    }
}


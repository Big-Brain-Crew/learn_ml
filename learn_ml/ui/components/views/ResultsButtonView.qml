import QtQuick 2.12

/* WORK IN PROGRESS - NOT BEING USED */

FocusScope {
    id: scope
    width: root.width
    height: root.height
    property alias color: root.color
    property alias radius: root.radius
    property alias text: buttonText.text
    property alias resultsButtonModel: root.resultsButtonModel
    
    Rectangle {
        id: root
        width: 300
        height: 40
        color: "#ffffff"
        radius: 5
        state: "defaultState"

        /// Public Interface ///

        /* Define with object creation */
        required property var resultsButtonModel

        /// End Public Interface ///

        readonly property var dispatcher: resultsButtonModel.dispatcher

        Text {
            id: buttonText
            color: "#000000"
            font.pointSize: 12
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            anchors.fill: parent

            text: resultsButtonModel.text
        }

        MouseArea {
            id: mouseArea
            anchors.fill: parent
            hoverEnabled: true
            onDoubleClicked: { 
                root.dispatcher.doubleClicked() 
            }
            onClicked: {
                root.dispatcher.clicked()
                root.state = "clickedState"
            }
        }

        states: [
            State {
                name: "defaultState"
                PropertyChanges {
                    target: root
                    color: "#ffffff"
                }
                PropertyChanges {
                    target: buttonText
                    color: "#000000"
                }
            },
            State {
                name: "hoveredState"
                when: mouseArea.containsMouse
                PropertyChanges {
                    target: root
                    color: "#62727b"
                }
                PropertyChanges {
                    target: buttonText
                    color: "#ffffff"
                }
            },
            State {
                name: "focusedState"
                when: scope.focus
                PropertyChanges {
                    target: root
                    color: "#62727b"
                }
                PropertyChanges {
                    target: buttonText
                    color: "#ffffff"
                }
            },
            State {
                name: "clickedState"
                PropertyChanges {
                    target: root
                    color: "#ff4081"
                }
                PropertyChanges {
                    target: buttonText
                    color: "#000000"
                }
            }
        ]
    }
}



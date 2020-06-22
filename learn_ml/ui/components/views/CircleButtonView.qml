import QtQuick 2.12

Rectangle {
    id: root

    /// Public Interface ///

    /* Define with object creation */
    required property var circleButtonModel

    /* Properties */
    width: 150
    height: 150
    color: "#37474f"
    radius: 100

    /// End Public Interface ///

    readonly property var dispatcher: circleButtonModel.dispatcher

    Text {
        id: text
        color: "#ffffff"
        font.pointSize: 15
        renderType: Text.NativeRendering
        font.family: "Roboto"
        fontSizeMode: Text.VerticalFit
        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter

        // From model
        text: circleButtonModel.text

    }

    MouseArea {
        anchors.fill: parent
        onClicked: {
            dispatcher.buttonPressed(text.text)
        }
    }
}
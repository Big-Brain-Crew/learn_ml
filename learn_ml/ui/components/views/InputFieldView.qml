import QtQuick 2.12

FocusScope {
    id: scope 
    width: root.width; height: root.height

    property alias color: root.color
    property alias text: textInput.text
    property alias inputFieldModel: root.inputFieldModel

    Rectangle {
        id: root
        width: 300
        height: 40
        color: "#ffffff"
        radius: 20

        /// Public Interface ///
        
        /* Define with object creation */
        required property var inputFieldModel

        /// End Public Interface

        /* Properties */
        readonly property var dispatcher: inputFieldModel.dispatcher

        TextInput {
            id: textInput
            x: 27
            y: 12
            width: root.width - 40
            height: root.height - 20
            text: qsTr("Search layer")
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignLeft
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            font.pixelSize: 12
            focus: true
            Keys.onPressed: {
                root.dispatcher.input(textInput.text)
            }
        }
    }
}




/*##^##
Designer {
    D{i:0;height:40;width:300}
}
##^##*/
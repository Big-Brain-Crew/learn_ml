import QtQuick 2.12
import QtQuick.Controls 2.15


FocusScope {
    id: scope 

    property alias color: background.color
    property alias text: textInput.text
    width: background.width; height: background.height

    signal pressed 

    Rectangle {
        id: background
        width: 300
        height: 40
        color: "#ffffff"
        radius: 20

        TextInput {
            id: textInput
            x: 27
            y: 12
            width: background.width - 40
            height: background.height - 20
            text: qsTr("Search layer")
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignLeft
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            font.pixelSize: 12
            focus: true
            Keys.onPressed: {
                scope.pressed()
            }
        }
    }
}




/*##^##
Designer {
    D{i:0;height:40;width:300}
}
##^##*/

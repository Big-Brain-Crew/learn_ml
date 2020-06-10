import QtQuick 2.12
//import ui 1.0

Item {
    width: parent.width
    height: parent.height

    Row {
        spacing: 100
        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter
        Rectangle {
            id: circle0
            anchors.verticalCenter: parent.verticalCenter
            width: 200
            height: 200
            color: "#37474f"
            radius: 100

            Text {
                id: circle0_text
                color: "#ffffff"
                text: "Make!"
                font.pointSize: 20
                renderType: Text.NativeRendering
                font.family: "Roboto"
                fontSizeMode: Text.VerticalFit
                anchors.verticalCenter: parent.verticalCenter
                anchors.horizontalCenter: parent.horizontalCenter
            }

            MouseArea {
                anchors.fill: parent
                onClicked: nav_buttons.buttonPressed(circle0_text.text);
            }
        }

        Rectangle {
            id: circle1
            anchors.verticalCenter: parent.verticalCenter
            width: 200
            height: 200
            color: "#37474f"
            radius: 100

            Text {
                id: cirlce1_text
                color: "#ffffff"
                text: "Train!"
                font.pointSize: 20
                renderType: Text.NativeRendering
                font.family: "Roboto"
                fontSizeMode: Text.VerticalFit
                anchors.verticalCenter: parent.verticalCenter
                anchors.horizontalCenter: parent.horizontalCenter
            }

            MouseArea {
                anchors.fill: parent
                onClicked: nav_buttons.buttonPressed(cirlce1_text.text);
            }
        }

        Rectangle {
            id: circle2
            anchors.verticalCenter: parent.verticalCenter
            width: 200
            height: 200
            color: "#37474f"
            radius: 100

            Text {
                id: cirlce2_text
                color: "#ffffff"
                text: "Deploy!"
                font.pointSize: 20
                renderType: Text.NativeRendering
                font.family: "Roboto"
                fontSizeMode: Text.VerticalFit
                anchors.verticalCenter: parent.verticalCenter
                anchors.horizontalCenter: parent.horizontalCenter
            }

            MouseArea {
                anchors.fill: parent
                onClicked: nav_buttons.buttonPressed(cirlce2_text.text);
            }
        }
    }
}

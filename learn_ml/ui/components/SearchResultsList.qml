import QtQuick 2.12

Rectangle {
    width: 300
    height: 150
    color: "#102027"

    Row {
        id: row
        anchors.fill: parent

        Rectangle {
            id: searchResult1
            height: 30
            color: "#ffffff"
            anchors.top: parent.top
            anchors.topMargin: 0
            border.width: 1
            anchors.right: parent.right
            anchors.rightMargin: 0
            anchors.left: parent.left
            anchors.leftMargin: 0

            Drag.active: dragArea.drag.active
            Drag.hotSpot.x: 10
            Drag.hotSpot.y: 10

            MouseArea {
                id: dragArea
                anchors.fill: parent

                drag.target: parent
            }

            Text {
                id: searchText1
                text: qsTr("Layer 1")
                verticalAlignment: Text.AlignVCenter
                anchors.fill: parent
                font.pixelSize: 18
            }
        }

        Rectangle {
            id: searchResult2
            height: 30
            color: "#ffffff"
            anchors.top: searchResult1.bottom
            anchors.topMargin: 0
            anchors.leftMargin: 0
            MouseArea {
                id: dragArea1
                anchors.fill: parent
                drag.target: parent
            }

            Text {
                id: searchText2
                text: qsTr("Layer 2")
                anchors.fill: parent
                verticalAlignment: Text.AlignVCenter
                font.pixelSize: 18
            }
            anchors.rightMargin: 0
            border.width: 1
            anchors.left: parent.left
            anchors.right: parent.right
            Drag.hotSpot.y: 10
            Drag.hotSpot.x: 10
        }

        Rectangle {
            id: searchResult3
            height: 30
            color: "#ffffff"
            anchors.top: searchResult2.bottom
            anchors.leftMargin: 0
            MouseArea {
                id: dragArea2
                anchors.fill: parent
                drag.target: parent
            }

            Text {
                id: searchText3
                text: qsTr("Layer 3")
                anchors.fill: parent
                verticalAlignment: Text.AlignVCenter
                font.pixelSize: 18
            }
            anchors.rightMargin: 0
            border.width: 1
            anchors.right: parent.right
            anchors.left: parent.left
            Drag.hotSpot.y: 10
            Drag.hotSpot.x: 10
            anchors.topMargin: 0
        }

        Rectangle {
            id: searchResult4
            height: 30
            color: "#ffffff"
            anchors.top: searchResult3.bottom
            anchors.leftMargin: 0
            MouseArea {
                id: dragArea3
                anchors.fill: parent
                drag.target: parent
            }

            Text {
                id: searchTest4
                text: qsTr("Layer 4")
                anchors.fill: parent
                verticalAlignment: Text.AlignVCenter
                font.pixelSize: 18
            }
            anchors.rightMargin: 0
            border.width: 1
            anchors.right: parent.right
            anchors.left: parent.left
            Drag.hotSpot.y: 10
            Drag.hotSpot.x: 10
            anchors.topMargin: 0
        }

        Rectangle {
            id: searchResult5
            height: 30
            color: "#ffffff"
            anchors.top: searchResult4.bottom
            anchors.leftMargin: 0
            MouseArea {
                id: dragArea4
                anchors.fill: parent
                drag.target: parent
            }

            Text {
                id: searchText5
                text: qsTr("Layer 5")
                anchors.fill: parent
                verticalAlignment: Text.AlignVCenter
                font.pixelSize: 18
            }
            anchors.rightMargin: 0
            border.width: 1
            anchors.right: parent.right
            anchors.left: parent.left
            Drag.hotSpot.y: 10
            Drag.hotSpot.x: 10
            anchors.topMargin: 0
        }
    }
}



/*##^##
Designer {
    D{i:2;anchors_height:30;anchors_width:250}D{i:5;anchors_height:30;anchors_width:250;anchors_y:100}
D{i:8;anchors_height:30;anchors_width:250;anchors_y:100}D{i:11;anchors_height:30;anchors_width:250;anchors_y:100}
D{i:14;anchors_height:30;anchors_width:250;anchors_y:100}D{i:1;anchors_height:400;anchors_width:200;anchors_x:0;anchors_y:0}
}
##^##*/

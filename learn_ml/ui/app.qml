import QtQuick 2.0
import QtQuick.Window 2.0

Window {
    width: 1920
    height: 1080
    visible: true
    title: "Hello Python World!"

    Rectangle {
        x: 0
        y: 0
        width: 1920
        height: 1080

        CircleNavigationBar {
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.verticalCenter: parent.verticalCenter
            id: circleNavigationBar
            x: 179
            y: 156
        }
    }
}

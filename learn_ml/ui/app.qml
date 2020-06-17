import QtQuick 2.0
import QtQuick.Window 2.0
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.0
import "components"

Window {
    id: root
    width: 1920
    height: 1080
    visible: true
    title: "Learn ML!"

    // Item {
    //     anchors.centerIn: parent
    //     width: 640
    //     height: 480

    //     Node {
    //         anchors.centerIn: parent
    //     }
    // }
    

    NodeCanvas {
        anchors.centerIn: parent
    }

    //  NodeManager {
    //         id: nodeManager
    //         anchors.fill: parent
    //     }

    // RowLayout {

    //     // NodeBar {
    //     //     id: nodeBar
    //     // }

    //     // CircleNavigationBar {
    //     //     x: 1920 / 2
    //     //     y: -400
    //     //     id: circleNavigationBar
    //     // }
    // }
}

/*##^##
Designer {
    D{i:0;formeditorZoom:0.33000001311302185}
}
##^##*/

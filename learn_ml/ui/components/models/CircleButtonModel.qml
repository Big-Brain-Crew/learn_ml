import QtQuick 2.12

Item {
    id: root

    /// Public Interface ///

    /* Define with object creation */
    property string text: "Default Text"
    property alias dispatcher: logicConnection.target

    /// End Public Interface ///

    Connections {
        id: logicConnection

        // function onButtonPressed(text) {
        //     console.log(text + " Button was pressed!")
        // }
    }
}


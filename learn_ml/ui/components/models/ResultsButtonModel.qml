import QtQuick 2.12

/* WORK IN PROGRESS - NOT BEING USED */


Item {
    id: root

    /// Public Interface ///
    
    /* Define with object creation */
    property alias dispatcher: logicConnection.target

    /* Properties */
    property string text: "Button"

    /// End Public Interface

    Connections {
        id: logicConnection
    }
}
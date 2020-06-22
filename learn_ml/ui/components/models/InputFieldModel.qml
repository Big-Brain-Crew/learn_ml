import QtQuick 2.12

Item {
    id: root

    /// Public Interface ///

    /* Define with object creation */
    property alias dispatcher: logicConnection.target

    /// End Public Interface ///


    Connections {
        id: logicConnection
    }
}
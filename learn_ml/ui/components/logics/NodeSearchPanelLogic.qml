import QtQuick 2.12

Item {
    id: root

    /// Public Interface ///

    /* Properties */
    readonly property alias inputFieldLogic: inputFieldLogic

    /* Signals */
    signal searchLayers(string input)
    signal selectNode(string name)

    /// End Public Interface ///

    InputFieldLogic {
        id: inputFieldLogic
    }

    Connections {
        id: inputFieldLogicConnection
        target: inputFieldLogic

        function onInput(input) {
            root.searchLayers(input)
        }
    }
}
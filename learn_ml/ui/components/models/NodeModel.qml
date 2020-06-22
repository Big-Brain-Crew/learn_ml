import QtQuick 2.12
import QtQuick.Controls 2.15

Item {
    id: root

    /// Public interface ///

    /* Define with object creation */
    // Connect to the Logic component
    property alias dispatcher: logicConnection.target

    /* Properties */
    property alias name: _.name
    property alias identifier: _.identifier
    readonly property alias parametersListModel: _.parametersListModel

    property var parameters: [
            {
                "name" : "param1",
                "type" : "string",
                "default" : "None",
                "required" : true
            }
        ]

    /// End Public Interface ///

    // Private properties
    Item {
        id: _

        property string name: "Node"
        property string identifier: "Node0"
        property alias parametersListModel: parametersListModel
    }

    ListModel {
        id: parametersListModel
        ListElement {
            parameterName: "name"
            parameterValue: "default"
        }
        ListElement {
            parameterName: "name2"
            parameterValue: "default2"
        }
    }

    onParametersChanged: {
        setNodeParameters()
    }

    Connections {
        id: logicConnection

        function onUpdateNodeParameterValue(identifier, parameterName, parameterValue) {
            updateNodeParameterValues(identifier, parameterName, parameterValue)
        }
    }

    /* Functions */

    // Update search results after new search is entered
    function setNodeParameters() {

        parametersListModel.clear()
        for (var i = 0; i < root.parameters.length; i++){
            parametersListModel.append({
                    "parameterName" : root.parameters[i]["name"],
                    "parameterValue" : root.parameters[i]["default"] === undefined ? "" : root.parameters[i]["default"]
                }
            )
        }
    }

    // Update parameter values when user inputs new values
    function updateNodeParameterValues(identifier, parameterName, parameterValue) {
        if (root.identifier == identifier) {
            for (var i = 0; i < root.parameters.length; i++){
                if (root.parameters[i]["name"] === parameterName){
                    root.parameters[i]["value"] = parameterValue
                }
            }
        }
    }
}
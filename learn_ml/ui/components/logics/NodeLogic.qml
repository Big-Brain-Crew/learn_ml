import QtQuick 2.12

Item {
    id: root
    property string test: "blah"

    signal updateNodeParameterValue(
        string identifier, string parameterName, string parameterValue)
}
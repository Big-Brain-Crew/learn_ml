import QtQuick 2.0
import QtQuick.Controls 2.15

// Python classes
import Search 1.0

Item {
    id: root

    /// Public interface ////

    /* Define with object creation */
    // Connect to the Logic component
    property alias dispatcher: logicConnection.target

    /* Properties */
    readonly property alias searchResultsModel: searchResultsModel
    readonly property alias inputFieldModel: inputFieldModel

    /* Signals */
    // Emitted when new search results are ready
    signal reResultsChanged(int number)

    /// End Public Interface ///

    // Private properties
    Item {
        id: _
    }

    // Search Panel API
    SearchPanel {
        id: searchPanel
    }

    InputFieldModel {
        id: inputFieldModel
        dispatcher: root.dispatcher.inputFieldLogic
    }

    // Store search results in list format
    // Dynamically adds results on a new input
    ListModel {
        id: searchResultsModel
        ListElement {
            result: "blah"
        }
        ListElement {
            result: "blah"
        }
        ListElement {
            result: "blah"
        }
    }

    /* Connections */

    Connections {
        id: logicConnection

        function onSearchLayers (input) {
            searchPanel.search(input)
        }

    }

    Connections {
        target: root
        function onReResultsChanged() { root.updateSearchResults() }
    }

    /* Functions */

    // Update search results after new search is entered
    function updateSearchResults() {
        searchResultsModel.clear()
        for (var i = 0; i < searchPanel.numResults; i++){
            searchResultsModel.append({
                "result" : searchPanel.results
            })
        }
    }

    // Connect signal to backend
    Component.onCompleted: searchPanel.resultsChanged.connect(reResultsChanged)
}
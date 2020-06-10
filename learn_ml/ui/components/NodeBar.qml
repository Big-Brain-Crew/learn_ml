import QtQuick 2.0
import QtQuick.Controls 2.15
import QtQuick.Extras 1.4
import QtQuick.Layouts 1.11

// Python classes
import Search 1.0

Rectangle {
    id: root
    width: 480
    height: 1080
    color: "#102027"
    border.color: "#102027"
    anchors.horizontalCenter: parent.horizontalCenter
    anchors.verticalCenter: parent.verticalCenter
    state: "initialState"

    signal nodeClicked

    FocusScope {
        id: mainView

        width: parent.width
        height: parent.height
        focus: true

        // Title display
        Text {
            id: titleText
            x: 86
            width: 300
            height: 75
            color: "#ffffff"
            text: qsTr("Layer Search")
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: parent.top
            anchors.topMargin: 20
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
            font.pixelSize: 50
        }

        // Custom search panel object
        // Generates search results based off user input
        // See SearchPanel.py for documentation
        SearchPanel {
            id: searchPanel
        }

        // User search input. Press enter to search
        SearchField {
            id: searchField
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: titleText.bottom
            anchors.topMargin: 25
            focus: true

            onPressed: {
                searchPanel.search(searchField.text)
                mainView.state = "searchState"
            }
            Keys.onTabPressed: { 
            searchResults.focus = true
            searchResults.currentIndex = 0
            }
            Keys.onDownPressed: { searchResults.focus = true }
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

        // Display search results
        ListView {
            id: searchResults
            width: 300
            height: 400
            anchors.top: searchField.bottom
            anchors.topMargin: 30
            anchors.horizontalCenter: parent.horizontalCenter
            clip: true // enable scrolling
            spacing: 5
            keyNavigationWraps: true
            currentIndex: -1

            model: searchResultsModel
            delegate: ResultsButton {
                id: resultsButton
                text: result
                onDoubleClicked: { root.nodeClicked() }
                Keys.onReturnPressed: { root.nodeClicked() }
            }

            Keys.onTabPressed: { incrementCurrentIndex() }
            Keys.onBacktabPressed: {
                if (currentIndex > 0)
                    decrementCurrentIndex()
                else
                    searchField.focus = true
            }
            Keys.onUpPressed: {
                if (currentIndex === 0)
                    searchField.focus = true
                else 
                    currentIndex--
            }
        }

        /* Signals */
        // Emitted when new search results are ready
        signal reResultsChanged(int number)
        Component.onCompleted: searchPanel.resultsChanged.connect(reResultsChanged)
        
        /* Root connections */
        Connections {
            target: mainView
            function onReResultsChanged() { mainView.updateSearchResults() }
        }

        /* states */
        states: [
            State {
                name: "initialState"
                PropertyChanges {
                    target: searchResults
                    visible: false
                }
            },
            State {
                name: "searchState"
                PropertyChanges {
                    target: searchResults
                    visible: true
                }
            }
        ]

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
    }
}


/*##^##
Designer {
    D{i:0;formeditorZoom:0.6600000262260437}D{i:2;anchors_x:363}D{i:5;anchors_x:30;anchors_y:115}
}
##^##*/

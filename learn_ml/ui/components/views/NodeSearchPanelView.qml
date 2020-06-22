import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Extras 1.4
import QtQuick.Layouts 1.11
import ".."
import "../delegates"

// Python classes
import Search 1.0

FocusScope {
    id: scope 
    width: 480
    height: 1080

    property alias color: root.color
    property alias nodeSearchPanelModel: root.nodeSearchPanelModel

    Rectangle {
        id: root
        width: parent.width
        height: parent.height
        color: "#37474f"
        border.color: "#37474f"
        state: "initialState"

        /// Public interface ///

        /* Define with object creation */
        required property var nodeSearchPanelModel
        
        /// End Public Interface ///

        readonly property var dispatcher: nodeSearchPanelModel.dispatcher

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

        // User search input. Press enter to search
        InputFieldView {
            id: searchFieldView
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: titleText.bottom
            anchors.topMargin: 25
            focus: true

            inputFieldModel: root.nodeSearchPanelModel.inputFieldModel

            Keys.onPressed: {
                if (event.key == Qt.Key_Tab || event.key == Qt.Key_Down) {
                    searchResults.focus = true
                    searchResults.currentIndex = 0
                }
                root.state = "searchState"
            }
        }
        
        // Display search results
        ListView {
            id: searchResults
            width: 300
            height: 400
            anchors.top: searchFieldView.bottom
            anchors.topMargin: 30
            anchors.horizontalCenter: parent.horizontalCenter
            clip: true // enable scrolling
            spacing: 5
            keyNavigationWraps: true
            currentIndex: -1
            
            model: root.nodeSearchPanelModel.searchResultsModel 
            delegate: ResultsButton {
                id: resultsButton
                text: result
                onDoubleClicked: { 
                    root.dispatcher.selectNode(text)
                }
                Keys.onReturnPressed: { 
                    root.dispatcher.selectNode(text) 
                }
            }

            Keys.onTabPressed: { 
                incrementCurrentIndex() 
            }
            Keys.onBacktabPressed: {
                if (currentIndex > 0)
                    decrementCurrentIndex()
                else
                    searchFieldView.focus = true
            }
            Keys.onUpPressed: {
                if (currentIndex === 0)
                    searchFieldView.focus = true
                else 
                    currentIndex--
            }
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
    }
}


/*##^##
Designer {
    D{i:0;formeditorZoom:0.6600000262260437}D{i:2;anchors_x:363}D{i:5;anchors_x:30;anchors_y:115}
}
##^##*/

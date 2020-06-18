import QtQuick 2.0
import QtQuick.Window 2.0
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import "components"

Window {
    id: root
    visible: true
    width: 1920
    height: 1080
    minimumWidth: 1000
    minimumHeight: 800
    title: "Learn ML!"

    // Main application top container page
    Page {
        id: page
        anchors.fill:parent
        title: "Main"

        // create a page loader to handle switching ui panels
        Loader {
            id: pageLoader
            source: {
                // load new page when slider get big
                (slider.value < 1) ? '' : 'components/WelcomePage.qml'
            }

            anchors.fill: parent

            // dinky funny slider demo to show the switching of pages
                Slider {
                    id: slider
                    x: 860
                    y: 76
                    value: 0
                }
            }
    }


 }

/*##^##
Designer {
    D{i:0;formeditorZoom:0.33000001311302185}
}
##^##*/

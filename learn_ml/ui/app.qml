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

    // Top level loader
   Loader{
       id: topLoader
       anchors.fill:parent
       source: "components/pages/WelcomePage.qml"

       Connections{
           target: topLoader.item
           function onOpenProject(sourceFile){
               topLoader.source = sourceFile

           }
       }
   }
}


/*##^##
Designer {
    D{i:0;formeditorZoom:0.33000001311302185}
}
##^##*/

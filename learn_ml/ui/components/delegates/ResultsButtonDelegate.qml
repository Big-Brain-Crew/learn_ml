import QtQuick 2.12
import "../views"
import "../models"
import "../logics"

Item {
    id: root

    /// Public Interface ///
    property alias text: resultsButtonModel.text 

    readonly property alias resultsButtonView: resultsButtonView
    readonly property alias resultsButtonModel: resultsButtonModel
    readonly property alias resultsButtonLogic: resultsButtonLogic

    /* Signals */
    signal doubleClicked()
    
    /// End Public Interface

    ResultsButtonView {
        id: resultsButtonView 
        resultsButtonModel: resultsButtonModel 
    }

    ResultsButtonModel {
        id: resultsButtonModel
        dispatcher: resultsButtonLogic
    }

    ResultsButtonLogic {
        id: resultsButtonLogic
    }

}



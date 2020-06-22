import QtQuick 2.12
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import "../views"
import "../logics"
import "../models"
import ".."

Item {
    id: root
    anchors.fill: parent

    ModelEditorPageView {
        id: modelEditorPageView
        modelEditorPageModel: modelEditorPageModel
    }

    ModelEditorPageModel {
        id: modelEditorPageModel
        dispatcher: modelEditorPageLogic
    }

    ModelEditorPageLogic {
        id: modelEditorPageLogic
    }
}
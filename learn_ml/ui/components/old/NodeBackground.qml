import QtQuick 2.0
import QtQuick.Window 2.0

Item {
    id: test
    visible: true
    //title: "Hello Python World!"


    Flickable {
        id: f
        anchors.fill: parent
        boundsBehavior: Flickable.StopAtBounds
        contentHeight: iContainer.height;
        contentWidth: iContainer.width;
        clip: true

        onContentXChanged: console.debug("CX"+contentX)
        onContentYChanged: console.debug("CY"+contentY)

        onAtXEndChanged: {
            console.log("X END CHANGED", f.atXEnd);
            if(f.atXEnd)
            {
                i.width += 100;
            }
        }

        //Behavior on contentY { NumberAnimation {} }
        //Behavior on contentX { NumberAnimation {} }

        property bool fitToScreenActive: true

        property real minZoom: 0.1;
        property real maxZoom: 2

        property real zoomStep: 0.1

        // Run when the width of the window is changed
        onWidthChanged: {
            if (fitToScreenActive)
                fitToScreen();
        }

        // Run when the height of the window is changed
        onHeightChanged: {
            if (fitToScreenActive)
                fitToScreen();
        }

        Item {
            id: iContainer

            // Width and height of the item containing the item
            // It is either the width of the containing flickable object, or the width of the image being displayed
            width: {
                console.log("Setting iContainer width");

                console.log(i.width * i.scale);
                console.log(f.width);
                console.log("Done setting iContainer height");
                console.log(Math.max(i.width * i.scale, f.width));
                return Math.max(i.width * i.scale, f.width);

            }
            height: Math.max(i.height * i.scale, f.height)

            Rectangle {
                id: i

                // Break the property binding so that the rectangle dimensions don't get updated every time window is resized
                Component.onCompleted: {
                    width  = 1000;
                    height = 1000;
                }

                anchors.centerIn: parent
                color: "#37474f"

                property real prevScale: 1.0;

                // This defines how many pixels / grid square
                property real gridDensity: 100

                // MouseArea {
                //     property vector2d dragStart
                //     acceptedButtons: Qt.LeftButton
                //     anchors.fill: parent
                //     onPressed: {
                //         dragStart = Qt.vector2d(mouseX, mouseY)
                //     }
                //     onReleased: {
                //         mouseRect.height = 0;
                //     }
                //     onPositionChanged: {
                //         if(pressed) {
                //         mouseRect.x = Math.min(mouseX, dragStart.x)
                //         mouseRect.width = Math.abs(mouseX - dragStart.x)
                //         mouseRect.y = Math.min(mouseY, dragStart.y)
                //         mouseRect.height = Math.abs(mouseY - dragStart.y)
                //         }
                //     }
                // }

                // Rectangle {
                //     id: mouseRect
                //     color: "#808080ff"
                //     }

                onWidthChanged: console.debug(width)
                onHeightChanged: console.debug(height)
                transformOrigin: Item.Center


                onScaleChanged: {
                    console.debug("Scale:", scale)
                    if ((width * scale) > f.width) {
                        var xoff = (f.width / 2 + f.contentX) * scale / prevScale;
                        f.contentX = xoff - f.width / 2
                    }
                    if ((height * scale) > f.height) {
                        var yoff = (f.height / 2 + f.contentY) * scale / prevScale;
                        f.contentY = yoff - f.height / 2
                    }
                    prevScale=scale;
                }

                Column {
                    anchors.fill: parent
                    Repeater {
                        model: Math.round(i.width / i.gridDensity)
                        Rectangle {
                            width: i.width
                            height: i.height / Math.round(i.width / i.gridDensity)
                            color: "transparent"
                            border {
                                color: "#62727b"
                                width: 1
                            }
                        }
                    }
                }

                Row {
                    anchors.fill: parent
                    Repeater {
                        model: Math.round(i.height / i.gridDensity)
                        Rectangle {
                            width: i.width / Math.round(i.height / i.gridDensity)
                            height: i.height
                            color: "transparent"
                            border {
                                color: "#62727b"
                                width: 1
                            }
                        }
                    }
                }

                Rectangle {
                    width: 50
                    height: 50
                    color: "#37474f"
                }
            }
        }
        function fitToScreen() {
            var s = Math.min(f.width / i.width, f.height / i.height, 1)
            i.scale = s;
            f.minZoom = s;
            i.prevScale = scale
            fitToScreenActive=true;
            f.returnToBounds();
        }
        function zoomIn() {
            console.log("ZOOM IN CALLED")
            if (f.scale<f.maxZoom)
                i.scale*=(1.0+zoomStep)
            f.returnToBounds();
            fitToScreenActive=false;
            f.returnToBounds();
        }
        function zoomOut() {
            console.log("ZOOM OUT CALLED")
            if (f.scale>f.minZoom)
                i.scale*=(1.0-zoomStep)
            else
                i.scale=f.minZoom;
            f.returnToBounds();
            fitToScreenActive=false;
            f.returnToBounds();
        }
        function zoomFull() {
            console.log("ZOOM FULL CALLED")
            i.scale=1;
            fitToScreenActive=false;
            f.returnToBounds();
        }

    }

    PinchArea {
        id: p
        anchors.fill: f
        enabled: true
        pinch.target: i
        pinch.maximumScale: 3
        pinch.minimumScale: 0.1
        onPinchStarted: {
            console.debug("PinchStart")
            f.interactive=false;
        }

        onPinchUpdated: {
            f.contentX += pinch.previousCenter.x - pinch.center.x
            f.contentY += pinch.previousCenter.y - pinch.center.y
        }

        onPinchFinished: {
            console.debug("PinchEnd")
            f.interactive=true;
            f.returnToBounds();
        }
    }

}

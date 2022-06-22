import QtQuick 2.15
import QtQuick.Shapes 1.15
import QtGraphicalEffects 1.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Styles 1.4
import QtQuick.Window 2.15

Item {
    id: card_item
    property string name: "NAME"
    property string component: "Cpu"
    property real percentage: 50
    //required property Item dragParent

    implicitHeight: 314
    implicitWidth: 212

    Rectangle {
        id: card

        anchors.fill: parent
        radius: 9
        gradient: Gradient {
            GradientStop {
                position: 0
                color: "#0d223f"
            }
            GradientStop {
                position: 0.5
                color: "#400f0934"
            }
        }

        /*DragHandler {
            id: dragHandler
        }

        Drag.active: dragHandler.active
        Drag.source: card_item
        Drag.hotSpot.x: 36
        Drag.hotSpot.y: 36

        states: [
            State {
                when: dragHandler.active
                ParentChange {
                    target: card_item
                    parent: card_item.dragParent
                }

                AnchorChanges {
                    target: card_item
                    anchors.horizontalCenter: undefined
                    anchors.verticalCenter: undefined
                }
            }
        ]*/

        ColumnLayout {
            spacing: 0
            width: 212
            RowLayout {
                width: 212

                id: row_layout
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                spacing: 0
                Layout.topMargin: 5
                Layout.bottomMargin: 5

                property int edge_width: 30

                Rectangle {
                    width: row_layout.edge_width
                    height: 15
                    color: "#00000000"
                }

                Text {
                    Layout.fillWidth: true
                    height: 30
                    id: name
                    color: "#BCBAB5"
                    font.pixelSize: 12
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    font.family: "Verdana"
                    text: qsTr(card_item.name)

                }
                Text {
                    width: row_layout.edge_width
                    height: 30
                    id: info
                    color: "#BCBAB5"
                    topPadding: 2
                    rightPadding: 10
                    font.pixelSize: 14
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                    font.styleName: "Bold"
                    font.family: "Verdana"
                    text: qsTr("ⓘ")
                }
            }
            Item {
                height: 280
                width: 212

                ColumnLayout {
                    width: 212
                    spacing: 12

                    Loader {
                        id: loader
                        Layout.alignment: Qt.AlignHCenter
                        source: card_item.component+"Component.qml"
                    }

                    Binding {
                        target: loader.item
                        property: "percentage"
                        value: card_item.percentage
                    }
                }
            }
        }
    }
}

/*##^##
Designer {
    D{i:0;autoSize:true;height:314;width:212}
}
##^##*/

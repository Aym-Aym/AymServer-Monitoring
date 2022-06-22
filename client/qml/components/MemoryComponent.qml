import QtQuick 2.15
import QtQuick.Layouts 1.15
import QtQuick.Shapes 1.15

Item {
    id: memory_component

    property real percentage: percentage

    implicitWidth: 212

    ColumnLayout {
        width: 212
        spacing: 12

        PercentageArcBar {
            percentage: memory_component.percentage
        }

        Item {
            Layout.alignment: Qt.AlignHCenter
            Layout.bottomMargin: 3
            Layout.topMargin: 10
            width:100
            height: 40

            RowLayout {
                anchors.fill: parent
                Shape {
                    ShapePath {
                        strokeColor: "#58B2DE"
                        strokeWidth: 6
                        capStyle: ShapePath.RoundCap
                        startX: 0
                        startY: 0
                        PathLine {
                            x: 0
                            y: 38
                        }
                    }
                }

                ColumnLayout {
                    Layout.alignment: Qt.AlignHCenter | Qt.AlignTop
                    spacing: 0

                    Text {
                        Layout.topMargin: -2
                        Layout.alignment: Qt.AlignHCenter
                        id: memory_name
                        text: qsTr("DDR3")
                        color: "#9F8851"
                        font.family: "Verdana"
                        font.pointSize: 12
                    }

                    Text {
                        Layout.alignment: Qt.AlignHCenter
                        id: core_number
                        text: qsTr("16Gb")
                        color: "#BCBAB5"
                        font.family: "Verdana"
                        font.pointSize: 10
                    }

                    Text {
                        Layout.alignment: Qt.AlignHCenter
                        id: logical_number
                        text: qsTr("1600 MHz")
                        color: "#BCBAB5"
                        font.family: "Verdana"
                        font.pointSize: 10
                    }
                }
            }
        }

        Charts {}
    }
}

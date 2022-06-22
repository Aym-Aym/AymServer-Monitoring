import QtQuick 2.15
import QtQuick.Window 2.15
import "components"
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Controls.Styles 1.4
import QtGraphicalEffects 1.15

Window {
        id: main_window
        width: 1194
        height: 834
        visible: true
        color: "#020431"
        title: qsTr("AymServer Monitoring")

        property real value_cpu: 100
        property real value_mem: 100
        RadialGradient {
            anchors.fill: parent

            verticalOffset: -(main_window.height/2)
            horizontalRadius: main_window.width - 50
            verticalRadius: main_window.height + 100

            gradient: Gradient {
                GradientStop {position: 0; color: "#003045"}
                GradientStop {position: 0.5; color: "#00000000"}
            }

            ColumnLayout {
                anchors.fill: parent

                ColumnLayout {
                    height: 47
                    Layout.alignment: Qt.AlignTop
                    Layout.topMargin: 18
                    spacing: -1

                    Text {
                        id: loool
                        color: "#BCBAB5"
                        text: qsTr("AymServer")
                        font.family: "verdana"
                        leftPadding: 116
                        font.pointSize: 30
                    }
                    Text {
                        id: loool2
                        color: "#9F8851"
                        text: qsTr("MONITORING")
                        font.family: "verdana"
                        leftPadding: 116
                        font.pointSize: 15
                    }
                }
                GridLayout {
                    Layout.alignment: Qt.AlignTop
                    Layout.leftMargin: 38
                    Layout.rightMargin: 38
                    Layout.fillHeight: true
                    columnSpacing: 15
                    layoutDirection: Qt.LeftToRight
                    flow: GridLayout.LeftToRight
                    columns: 5

                    Card {name: "CPU"; component: "Cpu"; percentage: value_cpu}
                    Card {name: "MEMORY"; component: "Memory"; percentage: value_mem}
                    Card {name: "SWAP"; component: "Memory"; percentage: value_mem}
                    Card {name: "SYSTEM"}
                    Card {name: "NETWORK"}
                    Card {name: "HDD1"}
                    Card {name: "HDD2"}
                }
                /*GridLayout {
                                    layoutDirection: Qt.LeftToRight
                                    flow: GridLayout.LeftToRight
                                    MonitorActivity {text_int: true; value: main_window.value_cpu}
                                    MonitorActivity {name: "MEM"; small: true; text_int: true; value: main_window.value_mem}
//                                    Charts {}
                                }


*/

            }

//
        }

}

import QtQuick 2.15
import QtQuick.Shapes 1.15
import QtGraphicalEffects 1.15
import QtQuick.Layouts 1.15
import QtQuick.Controls 2.15



Item {
    id: percentage_main
    property real percentage: 100

    QtObject {
        id: percentage_private

        property real delayed_value: percentage

        Behavior on delayed_value {
            NumberAnimation {
                duration: 500
            }
        }
    }

    Layout.alignment: Qt.AlignHCenter

    implicitHeight: 130
    implicitWidth: 150

        Shape {
            anchors.fill: parent
            layer.smooth: true
            focus: false
            antialiasing: false
            layer.enabled: true
            layer.samples: 8

            ShapePath {
                id: test
                fillColor: "#00000000"
                strokeColor: "#264563"
                strokeWidth: 4
                capStyle: ShapePath.RoundCap

                Behavior on strokeColor {
                    ColorAnimation {duration: 500}
                }

                PathAngleArc {
                    centerX: 150 / 2
                    centerY: 150 / 2
                    radiusX: (150 - test.strokeWidth) / 2 - 3
                    radiusY: (150 - test.strokeWidth) / 2 - 3
                    startAngle: 135
                    sweepAngle: 225
                }
            }
            ShapePath {
                id: test2
                fillColor: "#00000000"
                strokeColor: "#58B2DE"
                strokeWidth: 12
                capStyle: ShapePath.RoundCap

                Behavior on strokeColor {
                    ColorAnimation {duration: 500}
                }

                PathAngleArc {
                    centerX: 150 / 2
                    centerY: 150 / 2
                    radiusX: (150 - test2.strokeWidth) / 2
                    radiusY: (150 - test2.strokeWidth) / 2
                    startAngle: 135
                    sweepAngle: 225 * percentage_private.delayed_value / 100
                }
            }

            Text {
                anchors.fill: parent
                id: percent
                color: "#9F8851"
                text: parseInt(percentage_private.delayed_value)+"%"
                font.family: "Verdana"
                font.pointSize: 15
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                topPadding: 25
            }

    }
}

import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Shapes 1.15
import QtGraphicalEffects 1.15

Item {
    id: monitor_activity

    implicitHeight: 250
    implicitWidth: 250

    property string name: "CPU"
    property real radiusX: monitor_activity.small? 50: 100
    property real radiusY: monitor_activity.small? 50: 100
    property bool small: false
    property real startAngle: 135
    property real sweepAngle: 225
    property real value: 50
    property bool text_int: false

    QtObject {
        id: monitor_activity_private

        property real delayed_value: monitor_activity.value

        Behavior on delayed_value {
            NumberAnimation {
                duration: 500
            }
        }
    }

    Shape {
        anchors.fill: parent
        antialiasing: true
        layer.enabled: true
        layer.samples: 16

        ShapePath {
            fillColor: "#00000000"
            strokeColor: "#264563"
            strokeWidth: monitor_activity.small? 6: 12

            Behavior on strokeColor {
                ColorAnimation {duration: 500}
            }

            PathAngleArc {
                centerX: monitor_activity.width / 2
                centerY: monitor_activity.height / 2
                radiusX: monitor_activity.radiusX
                radiusY: monitor_activity.radiusY
                startAngle: monitor_activity.startAngle
                sweepAngle: monitor_activity.sweepAngle
            }
        }

        ShapePath {
            fillColor: "#00000000"
            strokeColor: monitor_activity.value <= 60? "#64cafc": monitor_activity.value <= 90? "#fcdb64": "#fc6464"
            strokeWidth: monitor_activity.small? 6: 12

            Behavior on strokeColor {
                ColorAnimation {duration: 500}
            }

            PathAngleArc {
                centerX: monitor_activity.width / 2
                centerY: monitor_activity.height / 2
                radiusX: monitor_activity.radiusX
                radiusY: monitor_activity.radiusY
                startAngle: monitor_activity.startAngle
                sweepAngle: ((monitor_activity_private.delayed_value <= 0.005? 0.005: monitor_activity_private.delayed_value) / 100) * monitor_activity.sweepAngle
            }
        }

//        ShapePath {
//            fillColor: "#00000000"
//            strokeColor: "grey"
//            strokeWidth: monitor_activity.small? 1: 2

//            PathAngleArc {
//                centerX: monitor_activity.width / 2
//                centerY: monitor_activity.height / 2
//                radiusX: monitor_activity.radiusX + (monitor_activity.small? 4: 8)
//                radiusY: monitor_activity.radiusY + (monitor_activity.small? 4: 8)
//                startAngle: 132.4
//                sweepAngle: 230.2
//            }
//        }

//        ShapePath {
//            fillColor: "#00000000"
//            strokeColor: "grey"
//            strokeWidth: monitor_activity.small? 1: 2

//            PathAngleArc {
//                centerX: monitor_activity.width / 2
//                centerY: monitor_activity.height / 2
//                radiusX: monitor_activity.radiusX - (monitor_activity.small? 4: 8)
//                radiusY: monitor_activity.radiusY - (monitor_activity.small? 4 :8)
//                startAngle: 132.4 - 180
//                sweepAngle: 230.2
//            }
//        }
    }

    Text {
        x: (monitor_activity.width / 2) -  (this.width / 2)
        y: monitor_activity.small? (monitor_activity.height / 2) - (this.height / 2) - 12 :(monitor_activity.height / 2) - (this.height / 2) - 13
        width: 91
        color: "white"
        text: monitor_activity.text_int? parseInt(monitor_activity_private.delayed_value)+"%": (monitor_activity_private.delayed_value).toFixed(2)+"%"
        horizontalAlignment: Text.AlignHCenter
        font.bold: false
        font.pointSize: monitor_activity.small? 15: 20
        font.family: "Verdana"
    }

    Text {
        x: (monitor_activity.width / 2) -  (this.width / 2)
        y: monitor_activity.small? (monitor_activity.height / 2) - (this.height / 2) + 5: (monitor_activity.height / 2) - (this.height / 2) + 11
        color: "white"
        text: monitor_activity.name
        horizontalAlignment: Text.AlignHCenter
        font.bold: true
        font.pointSize: monitor_activity.small? 25 : 40
        font.family: "Verdana"
    }
}

/*##^##
Designer {
    D{i:0;formeditorColor:"#4c4e50"}
}
##^##*/

import QtQuick 2.15
import QtQuick.Shapes 1.15
import QtGraphicalEffects 1.15
import QtQuick.Layouts 1.15
import QtCharts 2.3


Item {
    id: chart

    Layout.alignment: Qt.AlignHCenter
    width:190
    height: 70
    Rectangle {
        anchors.fill: parent
        color: "#00000000"
        border.color: "#264563"
        border.width: 1
        radius: 9

        RadialGradient {
            anchors.fill: parent

            verticalOffset: - (chart.height / 2)
            horizontalRadius: chart.width / 2
            verticalRadius: chart.height / 2

            gradient: Gradient {
                GradientStop {position: 0; color: "#0D223F"}
                GradientStop {position: 1; color: "#00000000"}
            }
        }
    }
}

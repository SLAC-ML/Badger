from PyQt5 import QtCore, QtGui, QtWidgets


stylesheet_toolbutton = """
QToolButton
{
    border: none;
}
"""


# https://stackoverflow.com/a/56293688
class ScrollArea(QtWidgets.QScrollArea):
    resized = QtCore.pyqtSignal()

    def resizeEvent(self, e):
        self.resized.emit()
        return super(ScrollArea, self).resizeEvent(e)


class Expander(QtWidgets.QWidget):
    def __init__(self, parent=None, title="", animationDuration=100):
        """
        References:
            # Adapted from PyQt4 version
            https://stackoverflow.com/a/37927256/386398
            # Adapted from c++ version
            https://stackoverflow.com/a/37119983/386398
        """
        super(Expander, self).__init__(parent=parent)

        self.animationDuration = animationDuration
        self.toggleAnimation = QtCore.QParallelAnimationGroup()
        self.contentArea = ScrollArea()
        self.toggleButton = QtWidgets.QToolButton()
        self.mainLayout = QtWidgets.QVBoxLayout(self)

        cool_font = QtGui.QFont()
        cool_font.setWeight(QtGui.QFont.DemiBold)
        cool_font.setPixelSize(13)

        toggleButton = self.toggleButton
        toggleButton.setFont(cool_font)
        toggleButton.setFixedHeight(28)
        toggleButton.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        toggleButton.setStyleSheet(stylesheet_toolbutton)
        toggleButton.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        toggleButton.setIconSize(QtCore.QSize(11, 11))
        toggleButton.setArrowType(QtCore.Qt.RightArrow)
        toggleButton.setText(str(title))
        toggleButton.setCheckable(True)
        toggleButton.setChecked(False)

        self.contentArea.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed
        )
        # start out collapsed
        self.contentArea.setMaximumHeight(0)
        self.contentArea.setMinimumHeight(0)
        self.contentArea.resized.connect(self.updateContentLayout)

        # let the entire widget grow and shrink with its content
        toggleAnimation = self.toggleAnimation
        toggleAnimation.addAnimation(QtCore.QPropertyAnimation(self, b"minimumHeight"))
        toggleAnimation.addAnimation(QtCore.QPropertyAnimation(self, b"maximumHeight"))
        toggleAnimation.addAnimation(
            QtCore.QPropertyAnimation(self.contentArea, b"maximumHeight")
        )

        mainLayout = self.mainLayout
        mainLayout.setSpacing(0)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.addWidget(self.toggleButton)
        mainLayout.addWidget(self.contentArea)

        def start_animation(checked):
            arrow_type = QtCore.Qt.DownArrow if checked else QtCore.Qt.RightArrow
            direction = (
                QtCore.QAbstractAnimation.Forward
                if checked
                else QtCore.QAbstractAnimation.Backward
            )
            toggleButton.setArrowType(arrow_type)
            self.toggleAnimation.setDirection(direction)
            self.toggleAnimation.start()

        self.toggleButton.clicked.connect(start_animation)

    def expand(self):
        if not self.toggleButton.isChecked():
            self.toggleButton.click()

    def updateContentLayout(self):
        if (
            self.toggleButton.isChecked()
            and self.toggleAnimation.state() != self.toggleAnimation.Running
        ):
            collapsedHeight = (
                self.sizeHint().height() - self.contentArea.maximumHeight()
            )
            contentHeight = self.contentArea.layout().sizeHint().height()
            self.setMinimumHeight(collapsedHeight + contentHeight)
            self.setMaximumHeight(collapsedHeight + contentHeight)
            self.contentArea.setMaximumHeight(contentHeight)
        self.updateGeometry()
        p = self.parent()
        if isinstance(p, ScrollArea):
            p.resized.emit()

    def setContentLayout(self, contentLayout):
        # Not sure if this is equivalent to self.contentArea.destroy()
        self.contentArea.destroy()
        self.contentArea.setLayout(contentLayout)
        collapsedHeight = self.sizeHint().height() - self.contentArea.maximumHeight()
        contentHeight = contentLayout.sizeHint().height()
        for i in range(self.toggleAnimation.animationCount() - 1):
            expandAnimation = self.toggleAnimation.animationAt(i)
            expandAnimation.setDuration(self.animationDuration)
            expandAnimation.setStartValue(collapsedHeight)
            expandAnimation.setEndValue(collapsedHeight + contentHeight)
        contentAnimation = self.toggleAnimation.animationAt(
            self.toggleAnimation.animationCount() - 1
        )
        contentAnimation.setDuration(self.animationDuration)
        contentAnimation.setStartValue(0)
        contentAnimation.setEndValue(contentHeight)

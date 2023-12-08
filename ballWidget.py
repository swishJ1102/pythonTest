import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QGraphicsScene, QGraphicsView, \
    QGraphicsEllipseItem
from PyQt5.QtCore import Qt


class BallWidget(QWidget):
    def __init__(self):
        super(BallWidget, self).__init__()

        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.view)
        # self.setLayout(self.layout)

        # self.ball = self.scene.addEllipse(0, 0, 50, 50, brush=Qt.red)
        self.ball = QGraphicsEllipseItem(0, 0, 50, 50)
        self.ball.setFlag(self.ball.ItemIsMovable)

        self.scene.addItem(self.ball)

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        position = event.pos()
        self.ball.setPos(self.view.mapToScene(position) - self.ball.rect().center())


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.central_widget = BallWidget()
        self.setCentralWidget(self.central_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())

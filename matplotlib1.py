import sys
import numpy as np
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolBar


class MatplotlibWidget(QWidget):
    def __init__(self):
        super(MatplotlibWidget, self).__init__()

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout = QVBoxLayout()
        self.layout.addWidget(NavigationToolBar(self.canvas, self))
        self.layout.addWidget(self.canvas)
        self.setLayout(self.layout)

        self.ax = self.figure.add_subplot(111, projection='3d')
        self.ax.set_xlim([-10, 10])
        self.ax.set_ylim([-10, 10])
        self.ax.set_zlim([-10, 10])
        # self.ball, = self.ax.plot([0], [0], [0], 'ro', markersize=10)
        self.scatter = self.ax.scatter([0], [0], [0], c='red', marker='o', s=100)
        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('motion_notify_event', self.on_drag)

        self.last_position = [0, 0, 0]

        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: None)
        self.timer.start(100)

    def on_press(self, event):
        if event.inaxes == self.ax:
            x, y, _ = self.last_position
            self.scatter.set_offsets([[x, y]])
            # self.ball.set_data([x], [y])
            # self.ball._offsets3d = ([x], [y], 0)
            self.canvas.draw_idle()

    def on_drag(self, event):
        if event.inaxes == self.ax:
            x, y, _ = self.last_position
            dx = event.xdata - x
            dy = event.ydata - y
            # self.ball.set_data([event.xdata], [event.ydata])
            self.scatter.set_offsets([[event.xdata, event.ydata]])
            # self.ball.set_3d_properties(self.last_position[2])
            # self.ball._offsets3d = ([event.xdata, event.ydata, 0])
            self.last_position = [event.xdata, event.ydata, 0]
            self.canvas.draw_idle()

            # self.last_position = [event.xdata, event.ydata, self.last_position[2]]


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.central_widget = MatplotlibWidget()
        self.setCentralWidget(self.central_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())

import sys
import numpy as np
from PySide2.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class MatplotlibWidget(QWidget):
    def __init__(self):
        super(MatplotlibWidget, self).__init__()

        self.figure, self.ax = plt.subplots(subplot_kw=dict(projection='3d'))
        self.canvas = FigureCanvas(self.figure)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.canvas)
        # self.setLayout(self.layout)

        # self.ball, = self.ax.plot([0], [0], [0], 'ro', markersize=10)
        self.scatter = self.ax.scatter([0], [0], [0], c='red', marker='o', s=100)
        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('motion_notify_event', self.on_drag)

        self.last_position = [0, 0, 0]

    def on_press(self, event):
        if event.inaxes == self.ax:
            x, y, _ = self.last_position
            # self.scatter.set_offsets([[x, y]])
            # self.ball.set_data([x], [y])
            self.scatter._offsets3d = ([x], [y], 0)
            self.canvas.draw_idle()

    def on_drag(self, event):
        if event.inaxes == self.ax:
            x, y, _ = self.last_position
            dx = event.xdata - x
            dy = event.ydata - y

            self.scatter._offsets3d = ([event.xdata, event.ydata, 0])
            self.last_position = [event.xdata, event.ydata, 0]
            self.ax.view_init(elev=20, azim=-45)
            self.canvas.draw_idle()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.central_widget = MatplotlibWidget()
        self.setCentralWidget(self.central_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    app.processEvents()
    sys.exit(app.exec_())

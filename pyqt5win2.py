import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QVBoxLayout, QPushButton, QLabel, QLineEdit


class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()

		self.setWindowTitle("Main Window")
		self.button = QPushButton("Open Another Window", self)
		self.button.clicked.connect(self.open_another_window)
		self.line = QLineEdit("", self)

	@staticmethod
	def open_another_window():
		dialog = AnotherDialog()
		dialog.exec_()


class AnotherDialog(QDialog):
	def __init__(self):
		super(AnotherDialog, self).__init__()

		self.setWindowTitle("Another Dialog")
		self.setGeometry(800, 600)

		label = QLabel("This is another dialog.", self)
		layout = QVBoxLayout(self)
		layout.addWidget(label)

		close_button = QPushButton("Close", self)
		close_button.clicked.connect(self.close)
		layout.addWidget(close_button)


if __name__ == "__main__":
	app = QApplication(sys.argv)
	main_window = MainWindow()
	main_window.show()
	sys.exit(app.exec_())

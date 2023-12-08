import sys

from PyQt5.QtCore import QDateTime, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox, QRadioButton, \
	QSlider, QComboBox, QTextEdit, QPushButton, QGroupBox, QProgressBar, QSpinBox, QDateEdit, QTimeEdit, QDateTimeEdit, \
	QListWidget


class EventHandling:
	def __init__(self):
		self.window = None
		self.timer = QTimer()
		self.timer.timeout.connect(self.update_datetime_edit)

	@staticmethod
	def on_label_click(self):
		print("label was clicked")

	@staticmethod
	def on_line_edit_return():
		print('line return was inputted')

	def set_window(self, window):
		self.window = window
		self.init_timer()

	def init_timer(self):
		self.timer.start(1000)

	def update_datetime_edit(self):
		if self.window:
			current_datetime = QDateTime.currentDateTime()
			self.window.datetime_edit.setDateTime(current_datetime)


class MyWindow(QWidget, EventHandling):
	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		main_layout = QVBoxLayout(self)
		label = QLabel("this is a label")
		label.mousePressEvent = lambda event: self.on_label_click(self)
		main_layout.addWidget(label)

		line_edit = QLineEdit()
		line_edit.returnPressed.connect(self.on_line_edit_return)
		main_layout.addWidget(line_edit)

		checkbox = QCheckBox('checkbox')
		main_layout.addWidget(checkbox)

		radio_button1 = QRadioButton('radio1')
		radio_button2 = QRadioButton('radio2')
		radio_layout = QHBoxLayout()
		radio_layout.addWidget(radio_button1)
		radio_layout.addWidget(radio_button2)
		main_layout.addLayout(radio_layout)

		slider = QSlider()
		main_layout.addWidget(slider)

		combo_box = QComboBox()
		combo_box.addItem('1')
		combo_box.addItem("2")
		main_layout.addWidget(combo_box)

		text_edit = QTextEdit()
		main_layout.addWidget(text_edit)

		button = QPushButton('button')
		main_layout.addWidget(button)

		process_bar = QProgressBar()
		process_bar.setValue(50)
		main_layout.addWidget(process_bar)

		spin_box = QSpinBox()
		main_layout.addWidget(spin_box)

		date_edit = QDateEdit()
		main_layout.addWidget(date_edit)

		time_edit = QTimeEdit()
		main_layout.addWidget(time_edit)

		datetime_edit = QDateTimeEdit()
		main_layout.addWidget(datetime_edit)
		# datetime_edit.setReadOnly(True)

		list_widget = QListWidget()
		list_widget.addItems(['1', '2', '3'])
		main_layout.addWidget(list_widget)

		group_box = QGroupBox('group')
		group_layout = QVBoxLayout(group_box)
		group_layout.addWidget(QPushButton('group button'))
		group_layout.addWidget(QLineEdit('group text'))
		main_layout.addWidget(group_box)

		self.set_window(self)

		self.setGeometry(100, 100, 800, 600)
		self.setWindowTitle("PyQt5")
		self.show()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = MyWindow()
	window.show()
	sys.exit(app.exec_())

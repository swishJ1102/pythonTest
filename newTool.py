import sys

from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import QApplication, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QListWidget, QProgressBar, \
	QPushButton, \
	QTableWidget, QVBoxLayout, QWidget


class ButtonClickHandler:
	def handle_click(self):
		print("clicked!!!!")


class MyApp(QWidget):
	def __init__(self):
		super().__init__()

		self.button_click_handler = ButtonClickHandler()
		self.init_ui()

	def init_ui(self):
		top_group = QGroupBox("top")
		top_layout_1 = QHBoxLayout()
		top_layout_2 = QHBoxLayout()
		top_layout = QVBoxLayout()
		label_before = QLabel('Label')
		input_field_before = QLineEdit()
		button_before = QPushButton('Button')
		label_after = QLabel('Label')
		input_field_after = QLineEdit()
		button_after = QPushButton('Button')
		button_before.clicked.connect(self.button_click_handler.handle_click)

		top_layout_1.addWidget(label_before)
		top_layout_1.addWidget(input_field_before)
		top_layout_1.addWidget(button_before)
		top_layout_2.addWidget(label_after)
		top_layout_2.addWidget(input_field_after)
		top_layout_2.addWidget(button_after)
		top_layout.addLayout(top_layout_1)
		top_layout.addLayout(top_layout_2)
		top_group.setLayout(top_layout)

		bottom_left_group = QGroupBox('bottom left')
		bottom_left_layout = QVBoxLayout()
		list_widget = QListWidget()

		bottom_left_layout.addWidget(list_widget)
		bottom_left_group.setLayout(bottom_left_layout)

		bottom_right_group = QGroupBox('bottom right')
		bottom_right_layout = QVBoxLayout()
		table_widget = QTableWidget()
		table_widget.setColumnCount(2)
		table_widget.setHorizontalHeaderLabels(['Col1', 'Col2'])

		bottom_right_layout.addWidget(table_widget)
		bottom_right_group.setLayout(bottom_right_layout)

		bottom_layout = QHBoxLayout()
		bottom_layout.addWidget(bottom_left_group)
		bottom_layout.addWidget(bottom_right_group)

		button_group = QGroupBox("button")
		button_layout = QHBoxLayout()
		exec_button = QPushButton('Exec Button')
		save_button = QPushButton('Save Button')
		exit_button = QPushButton('Exit Button')

		button_layout.addWidget(exec_button)
		button_layout.addWidget(save_button)
		button_layout.addWidget(exit_button)
		button_group.setLayout(button_layout)

		tips_group = QGroupBox("tips")
		tips_layout = QHBoxLayout()
		self.tips_label = QLabel('Label')
		progress_bar = QProgressBar()
		tips_layout.addWidget(self.tips_label)
		tips_layout.addWidget(progress_bar)
		tips_group.setLayout(tips_layout)

		main_layout = QVBoxLayout()
		main_layout.addWidget(top_group)
		main_layout.addLayout(bottom_layout)
		main_layout.addWidget(button_group)
		main_layout.addWidget(tips_group)

		self.setLayout(main_layout)
		self.setWindowTitle('show')
		self.setGeometry(100, 100, 800, 600)
		self.timer_init()

	def timer_init(self):
		print(f'timer_init start...')
		timer = QTimer()
		print(f'timer_init start1...')
		timer.timeout.connect(self.update_datetime)
		print(f'timer_init start2...')
		timer.start(1000)
		print(f'timer_init start3...')
		current_datetime = QDateTime.currentDateTime().toString(Qt.ISODate)
		self.tips_label.setText(current_datetime)

	def update_datetime(self):
		print(f'update_datetime_and_progress start...')
		current_datetime = QDateTime.currentDateTime().toString(Qt.ISODate)
		print(f'Current DateTime : {current_datetime}')
		self.tips_label.setText(f'Current DateTime : {current_datetime}')


if __name__ == '__main__':
	app = QApplication(sys.argv)
	my_app = MyApp()
	my_app.show()
	sys.exit(app.exec_())

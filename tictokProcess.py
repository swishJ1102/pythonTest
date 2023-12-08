import os
import sys

from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox, \
	QRadioButton, \
	QSlider, QComboBox, QTextEdit, QPushButton, QGroupBox, QProgressBar, QSpinBox, QDateEdit, QTimeEdit, QDateTimeEdit, \
	QListWidget
from tkinter import filedialog


class EventHandling:
	def __init__(self):
		pass

	# self.timer = QTimer()
	# self.timer.timeout.connect(self.update_datetime_and_progress)
	# self.timer.start(1000)

	# def update_datetime_and_progress(self):
	# 	current_datetime = QDateTime.currentDateTime().toString(Qt.ISODate)
	# 	self.label.setText(f'Current DateTime : {current_datetime}')
	# 	current_value = self.progress_bar.value()
	#
	# 	if current_value < 100:
	# 		self.progress_bar.setValue(current_value + 1)
	# 	else:
	# 		self.timer.stop()
	# 		self.show_completion_popup()

	def show_completion_popup(self):
		QMessageBox.information(self, "Task Completed", "Process completed successfully!")


class MyWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.source_file_path = None
		self.current_value = None
		self.process_count = None
		self.timer_show_files = None
		self.count = None
		self.files_list = None
		self.file_path = None
		self.folder_path = None
		self.list_widget = None
		self.button = None
		self.line_edit = None
		self.timer = None
		self.process_bar = None
		self.label = None
		self.group_layout = None
		self.group_box = None
		self.main_layout = None
		self.initUI()

	def initUI(self):
		self.main_layout = QVBoxLayout(self)

		self.line_edit = QLineEdit()
		self.main_layout.addWidget(self.line_edit)
		self.button = QPushButton('button')
		self.main_layout.addWidget(self.button)
		self.button.clicked.connect(self.on_button_click)

		self.group_box = QGroupBox('group')
		self.group_layout = QVBoxLayout(self.group_box)
		self.list_widget = QListWidget()
		self.list_widget.addItems(['1', '2', '3'])

		self.main_layout.addWidget(self.list_widget)
		self.group_layout.addWidget(self.label)
		self.process_bar = QProgressBar()
		self.process_bar.setMinimum(0)
		self.process_bar.setMaximum(100)
		# self.process_bar.setValue(1)
		self.group_layout.addWidget(self.process_bar)
		self.main_layout.addWidget(self.group_box)

		self.label = QLabel("")
		self.main_layout.addWidget(self.label)

		self.setGeometry(100, 100, 600, 300)
		self.setWindowTitle("tictok")
		self.timer_init()

	def timer_init(self):
		self.timer = QTimer()
		self.timer.timeout.connect(self.update_datetime_and_progress)
		self.timer.start(1000)

	def update_datetime_and_progress(self):
		current_datetime = QDateTime.currentDateTime().toString(Qt.ISODate)
		self.label.setText(f'Current DateTime : {current_datetime}')

	# print(f'Current DateTime : {current_datetime}')
	# current_value = self.process_bar.value()
	# print(f'current_value : {current_value}')

	# if current_value < 100:
	# 	self.process_bar.setValue(current_value + 1)
	# else:
	# 	self.timer.stop()
	# 	self.show_completion_popup()

	def show_completion_popup(self):
		QMessageBox.information(self, "Task Completed", "Process completed successfully!")

	def on_button_click(self):
		self.folder_path = filedialog.askdirectory()
		if self.folder_path:
			self.line_edit.clear()
			self.line_edit.setText(self.folder_path)
		self.show_files_in_tree()

	def show_files_in_tree(self):
		self.count = self.total_num_cal()
		self.timer_show_files = QTimer()
		self.timer_show_files.timeout.connect(self.update_progress)
		self.timer_show_files.start(1)
		print(f'show_files_in_tree start...{self.count}')
		self.file_path = self.line_edit.text()
		# print(f'file_path : {self.file_path}')
		self.files_list = os.listdir(self.file_path)
		# print(f'files_list : {self.files_list}')
		self.list_widget.clear()
		self.process_count = 0
		for root, _, files in os.walk(self.file_path):
			# print(f'files : {files}')
			for filename in files:
				# print(f'filename : {filename}')
				self.source_file_path = os.path.join(root, filename)
				if os.path.isfile(self.source_file_path):
					self.update_progress()
					self.process_count += 1

	def update_progress(self):
		self.list_widget.addItem(self.source_file_path)
		self.list_widget.scrollToBottom()
		print(f'update_progress : {self.process_count} --- {self.count}')
		self.current_value = self.process_count / self.count * 100
		print(f'current_value : {self.current_value}')
		self.process_bar.setValue(int(self.current_value))

		if self.current_value < 100:
			pass
		# self.process_bar.setValue(self.current_value)
		# self.process_bar.setValue(100)
		elif self.current_value == 100:
			print(f'show_completion_popup : {self.current_value}')
			self.show_completion_popup()
			self.timer_show_files.stop()
		else:
			self.timer_show_files.stop()

	def total_num_cal(self):
		self.count = 0
		self.file_path = self.line_edit.text()
		self.files_list = os.listdir(self.file_path)
		for root, _, files in os.walk(self.file_path):
			for filename in files:
				source_file_path = os.path.join(root, filename)
				if os.path.isfile(source_file_path):
					self.count += 1
		return self.count


if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = MyWindow()
	window.show()
	sys.exit(app.exec_())

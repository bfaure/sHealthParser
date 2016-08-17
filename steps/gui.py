# PyQt4 modules
import PyQt4
from PyQt4 import QtGui
from PyQt4.QtCore import QThread, QRect
from PyQt4 import QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import sys
import data


class execution_thread(QThread):
	# Thread to handle the calculations and inferface with the Keras classification modules.
	def __init__(self):
		QThread.__init__(self)

	def loadStepData(self):
		self.step_data_files = data.getFileNames()
		# Only loading in the first file for now
		self.step_data = data.stepData(data.readEntries(self.step_data_files[0]))
		self.emit(SIGNAL("send_data(PyQt_PyObject)"), self.step_data)
		
	def run(self):
		# Logic goes here
		self.loadStepData()

class window(QtGui.QWidget):

	def __init__(self, parent=None):
		super(window, self).__init__()
		self.initThread()
		self.initUI()

	def initThread(self):
		# Initializes the thread and starts its execution (loading in the model)
		self.thread = execution_thread()


	def initUI(self):
		self.setFixedHeight(400)
		self.setFixedWidth(900)
		self.setWindowTitle("sHealth Step Viewer")

		self.status = QtGui.QLabel("Loading step data...", self)
		self.status.setFixedWidth(300)
		self.status.move(10, 10)

		self.entrySelector = QtGui.QListWidget(self)
		self.entrySelector.move(10, 40)
		self.entrySelector.itemClicked.connect(self.entrySelected)

		self.calorieLabel = QLabel("Calories Burned", self)
		self.calorieLabel.setFixedWidth(150)
		self.calorieLabel.move(350, 50)

		self.calorieValue = QLineEdit(" ", self)
		self.calorieValue.setFixedWidth(100)
		self.calorieValue.move(450, 50)
		self.calorieValue.setEnabled(False)

		self.stepLabel = QLabel("Steps", self)
		self.stepLabel.setFixedWidth(150)
		self.stepLabel.move(350, 100)

		self.stepValue = QLineEdit(" ", self)
		self.stepValue.setFixedWidth(100)
		self.stepValue.move(450, 100)
		self.stepValue.setEnabled(False)

		self.distLabel = QLabel("Distance", self)
		self.distLabel.setFixedWidth(150)
		self.distLabel.move(350, 150)

		self.distValue = QLineEdit(" ", self)
		self.distValue.setFixedWidth(100)
		self.distValue.move(450, 150)
		self.distValue.setEnabled(False)

		self.speedLabel = QLabel("Average Speed", self)
		self.speedLabel.setFixedWidth(150)
		self.speedLabel.move(350, 200)

		self.speedValue = QLineEdit(" ", self)
		self.speedValue.setFixedWidth(100)
		self.speedValue.move(450, 200)
		self.speedValue.setEnabled(False)

		self.show()
		QtCore.QObject.connect(self.thread, QtCore.SIGNAL("send_data(PyQt_PyObject)"), self.setData)
		self.thread.start()

	def setData(self, step_data):
		self.status.setText("Step data loaded successfully")
		self.data = step_data
		self.entries = step_data.getNames()
		self.entrySelector.addItems(self.entries)

	def entrySelected(self):
		print("Entry selected")





def main():

	app = QtGui.QApplication(sys.argv)
	_ = window()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()
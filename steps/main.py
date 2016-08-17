import sys
from os import listdir
from os.path import isfile, join

DATA_FOLDER = "data"

class stepData:
	# Holds a grouping of step entries

	def __init__(self, entries):
		self.data 	 = entries
		self.resetMetaData()

	def resetMetaData(self):
		self.stepsAcc 		= False
		self.distAcc  		= False
		self.avgSpeedAcc 	= False
		self.calorieAcc		= False

	def addData(self, newData):
		self.resetMetaData()
		self.data = self.data + newData # Append the new data

	def totalSteps(self):
		if hasattr(self, "steps") and self.stepsAcc==True:
			return self.steps

		self.steps = 0 # Initialize step count

		for entry in self.data:
			# Add up total step count
			self.steps += int(entry.count)

		self.stepsAcc = True
		return self.steps

	def totalDistance(self):
		if hasattr(self, "dist") and self.distAcc==True:
			return self.dist

		self.dist = 0

		for entry in self.data:
			self.dist += float(entry.distance)

		self.distAcc = True
		return self.dist

	def totalCalories(self):
		if hasattr(self, "calorie") and self.calorieAcc==True:
			return self.calorie

		self.calorie = 0

		for entry in self.data:
			self.calorie += float(entry.calorie)

		self.calorieAcc = True
		return self.calorie

	def avgSpeed(self):
		if hasattr(self, "avgSpeed") and self.avgSpeedAcc==True:
			return self.avgSpeed

		totalSpeed = 0

		for entry in self.data:
			totalSpeed += float(entry.speed)

		self.avgSpeed = float(totalSpeed / len(self.data))
		self.avgSpeedAcc = True
		return self.avgSpeed

	def printMetaData(self):
		print "Step count       = "+str(self.totalSteps())
		print "Total distance   = "+str(self.totalDistance())+" feet"
		print "Calories burned  = "+str(self.totalCalories())
		print "Average speed    = "+str(self.avgSpeed())+" mph"

class stepEntry:
	# Holds a single step entry
	
	def __init__(self, fileLine):

		self.members = ["time_offset","end_time","speed","pkg_name","start_time","count","sample_position_type","calorie","distance","datauuid","deviceuuid","update_time","create_time"]
		cur_position = 0 # The first element iterator

		for cur_member in self.members:
			comma 						= fileLine.find(",", cur_position) # The next comma location
			data 						= fileLine[cur_position:comma] # The data between commas
			self.__dict__[cur_member] 	= data
			cur_position 				= comma+1

	def printEntry(self):
		for member in self.members:
			print(member+": "+self.__dict__[member])

def getFileNames():
	# return a list of all filenames in the /data folder

	directory = DATA_FOLDER

	# List of every filename
	files = listdir(directory)
	# List of the paths to all the files
	paths = []

	for file in files:
		# Fill the paths list with full filenames
		if file.find(".csv") != -1:
			# As long as it is the correct filetype
			paths.append(directory+"/"+file)

	if len(paths) == 0:
		print("There is nothing in the data folder")
		sys.exit()

	return paths

def readEntries(filename, numEntries=10000000):

	print "Reading step data..."

	entries = [] # List of stepEntry structs

	f = open(filename)
	f.readline() # Skip the file name header
	f.readline() # Skip the naming header

	last_position = 0

	for _ in range(numEntries): # Get the requested entries

		cur = f.readline() # Get the next line

		if f.tell() == last_position: # If we are at the end of the file
			print "Reached the end of the file, found "+str(len(entries))+" entries."
			return entries

		entries.append(stepEntry(cur))
		last_position = f.tell()

	return entries

def main():
	# first we will check for files in the /data folder
	files = getFileNames()

	steps = readEntries(files[0])

	data = stepData(steps)

	data.printMetaData()


if __name__ == '__main__':
	main()
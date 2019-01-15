from pathlib import Path
import csv

class DataManager:
	""" Manager takes data from CSV file. """

	def __init__(self, filename):
		""" Take name of the file. """
		self.filename = filename + ".csv"
		self.path = Path(self.filename)
		self.nameRow = ["Game name", "MMO", "Simulator", "Adventure", "RTS", "Puzzle", "Action", "Stealth", "Combat", "FPS", "Sport", "RPG", "Education"]
		self.data = []
		self.readData()

	def createFile(self):
		""" Create data file. """
		with open(self.filename, 'w') as csvfile:
		    writer = csv.writer(csvfile)
		    writer.writerow(self.nameRow)
		    self.data.clear()

	def addGameItem(self, item):
		""" Adding item to data file. """
		if not self.path.is_file():
			self.createFile()
		with open(self.filename, "a") as csvfile:
			writer = csv.writer(csvfile)
			writer.writerow(item)
			self.data.append(item)

	def updateDataFile(self):
		""" Removing item from data file. """
		if not self.path.is_file():
			self.createFile()
		with open(self.filename, "w") as csvfile:
			writer = csv.writer(csvfile)
			writer.writerow(self.nameRow)
			writer.writerows(self.data)

	def readData(self):
		""" Read data from file. """
		if not self.path.is_file():
			return
		self.data.clear()
		with open(self.filename) as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				if row != self.nameRow and len(row) > 0:
					self.data.append(row)
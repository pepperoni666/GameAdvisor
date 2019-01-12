from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
import csv
 
class DataManager:
	""" Manager takes data from CSV file. """

	def __init__(self, filename):
		""" Take name of the file. """
		self.filename = filename + ".csv"
		self.nameRow = ["Game name", "MMO", "Simulator", "Adventure", "RTS", "Puzzle", "Action", "Stealth", "Combat", "FPS", "Sport", "RPG", "Education"]
		self.data = []
		self.readData()

	def createFile(self):
		""" Create data file. """
		with open(self.filename, 'w') as csvfile:
		    writer = csv.writer(csvfile)
		    writer.writerow(self.nameRow)

	def readData(self):
		""" Read data from file. """
		with open(self.filename) as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				if row != self.nameRow:
					self.data.append(row)


class AnswerBuilder:
	""" Builds answer from given data. """

	def __init__(self):
		""" Initialize empty answer. """
		self.types = []

	def isNotEmptyAnswer(self):
		""" Checks are there any types already. """
		if len(self.types) is 0:
			return False
		return True

	def clearTypes(self):
		""" Delete all stored types from answer builder. """
		self.types.clear()

	def addType(self, type):
		""" Adds type to answer builder. """
		self.types.append(type)

	def getAnswer(self, dataManager):
		""" Create and return answer. """
		typesNums = []
		for i in range(len(dataManager.nameRow)):
			if dataManager.nameRow[i] in self.types:
				typesNums.append(i)
		top = {}
		for row in dataManager.data:
			if len(row) is 0:
				continue
			p = 0
			for i in range(1, len(row)):
				if i in typesNums:
					p+=int(row[i])
			top[row[0]] = p
		top_sorted_values = sorted(top.items(), key=lambda kv: kv[1], reverse=True)
		result = ""
		for i in range(0, len(top_sorted_values)):
			if top_sorted_values[i][1] is len(typesNums):
				break
			result += str(i+1) + ". " + top_sorted_values[i][0] + "\t\t\t\t\t(" + str(top_sorted_values[i][1]) + "p)" + "\n"
		return result


class Application(Frame):
	""" A GUI application. """

	def __init__(self, master):
		""" Initialize the Frame. """
		Frame.__init__(self, master)
		self.grid()
		self.dataManager = DataManager("Games")
		self.gameTypesCheckDict = dict.fromkeys(self.dataManager.nameRow)
		del self.gameTypesCheckDict[self.dataManager.nameRow[0]]
		self.create_widgets()
		self.answerBuilder = AnswerBuilder()
		#self.dataManager.createFile()


	def create_widgets(self):
		""" A GUI application"""
		self.label = Label(self, text = "Choose catigories:", font=("Arial Bold", 15))
		self.label.grid(row = 0, columnspan=4, pady= 8)
		r = 0
		c = 0
		for i in self.gameTypesCheckDict:
			self.gameTypesCheckDict[i] = BooleanVar()
			if r > 2:
				c+=1
				r=0
			r+=1
			Checkbutton(self, text = i, font=("Arial", 11), variable = self.gameTypesCheckDict[i]).grid(row = r, column = c, sticky = W, padx=9)
		self.submit = Button(self, text = "Advise", command = self.submit)
		r+=1
		self.submit.grid(row = r, columnspan=4, pady= 8)
		self.answer = scrolledtext.ScrolledText(self, width=45, height=15)
		r+=1
		self.answer.grid(row = r, columnspan=4, pady = 12)

	def submit(self):
		""" Action on 'Advise' button. """
		self.answerBuilder.clearTypes()
		for i in self.gameTypesCheckDict:
			if self.gameTypesCheckDict[i].get():
				self.answerBuilder.addType(i)
		if self.answerBuilder.isNotEmptyAnswer():
			self.answer.delete(1.0, END)
			self.answer.insert(INSERT, self.answerBuilder.getAnswer(self.dataManager))
		else:
			self.showMessage("Title", "Fuck you!")

	def showMessage(self, title, message):
		""" Creates messageBox with given title and message. """
		messagebox.showinfo(title, message)


window = Tk()
 
window.title("Game Advisor")

window.geometry('450x440')

app = Application(window)

window.mainloop()
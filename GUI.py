from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import Menu
from tkinter import ttk
from dataManager import DataManager
from answerBuilder import AnswerBuilder

class Application(Tk):
	""" A GUI application. """

	def __init__(self):
		""" Initialize the Frame. """
		Tk.__init__(self)
		self.title("Game Advisor")
		self.geometry('450x480')
		self.grid()
		self.dataManager = DataManager("Games")
		self.gameTypesCheckDict = dict.fromkeys(self.dataManager.nameRow)
		del self.gameTypesCheckDict[self.dataManager.nameRow[0]]
		self.create_widgets()
		self.answerBuilder = AnswerBuilder()


	def create_widgets(self):
		""" A GUI application"""
		menu = Menu(self)
		new_item1 = Menu(menu)
		new_item1.add_command(label='Create file', command = self.createFile)
		new_item1.add_command(label='Data file changed', command = self.dataFileChanged)
		menu.add_cascade(label='File', menu=new_item1)
		new_item2 = Menu(menu)
		new_item2.add_command(label='Add game', command=self.addGame)
		new_item2.add_command(label='Remove game', command=self.removeGames)
		new_item2.add_command(label='Edit games', command=self.editGames)
		menu.add_cascade(label='Data', menu=new_item2)
		self.config(menu=menu)
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
		self.radioSelected = StringVar()
		self.radioSelected.set("and")
		r+=1
		self.radioAnd = Radiobutton(self,text='AND', indicatoron = 0, width = 10, value="and", variable=self.radioSelected)
		self.radioAnd.grid(row = r, column = 1, sticky = E, pady= 8)
		self.radioOr = Radiobutton(self,text='OR', indicatoron = 0, width = 10, value="or", variable=self.radioSelected)
		self.radioOr.grid(row = r, column = 2, sticky = W, pady= 8)
		self.submit = Button(self, text = "Advise", font=("Arial Bold", 12), width = 20, command = self.submit)
		r+=1
		self.submit.grid(row = r, columnspan=4, pady= 8)
		self.answer = scrolledtext.ScrolledText(self, width=45, height=15)
		r+=1
		self.answer.grid(row = r, columnspan=4, pady = 12)

	def createFile(self):
		""" on File->Create_file clicked"""
		result = messagebox.askquestion("Create file", "You trying to create new data file.\nIf it already exists, all data will be deleted from it!\nAre you shure?", icon='warning')
		if result == "yes":
			self.dataManager.createFile()

	def dataFileChanged(self):
		""" on File->Data_file_changed clicked"""
		self.dataManager.readData()
		messagebox.showinfo("Success", "Data was successfully updated!")

	def addGame(self):
		""" Open window with add item form. """
		self.window = Tk()
		self.window.title("Add game")
		self.window.geometry('910x180')
		self.window.grid()
		Label(self.window, text = "Create item", font=("Arial Bold", 15)).grid(row = 0, columnspan=len(self.dataManager.nameRow), pady= 8)
		c = 0
		for i in self.dataManager.nameRow:
			Label(self.window, text = i, padx=7, borderwidth=2, relief="groove", font=("Arial", 12)).grid(row=1, column=c)
			c+=1
		self.newGameName = Entry(self.window,width=15)
		self.newGameName.grid(row = 2, column = 0)
		self.combobox = []
		for i in range(1, len(self.dataManager.nameRow)):
			com = ttk.Combobox(self.window, width = 3)
			com['values'] = (1, 2, 3, 4, 5)
			com.current(0)
			com.grid(row=2, column = i)
			self.combobox.append(com)
		Button(self.window, text = "Add item", font=("Arial Bold", 12), width = 20, command = self.addItem).grid(row = 3, columnspan=len(self.dataManager.nameRow), pady= 15)
		self.window.mainloop()

	def createListBox(self, root, sm):
		""" Creates list-view of all games stored. """
		gameList = Listbox(root, height = 20, width = 40, font = ("Arial", 11), selectmode = sm)
		n = 1
		for i in self.dataManager.data:
			if len(i) > 0:
				gameList.insert(n, i[0])
				n+=1
		return gameList

	def addItem(self):
		""" Add new game to data file"""
		if len(self.newGameName.get()) < 1:
			return
		newItem = []
		newItem.append(self.newGameName.get())
		for i in self.combobox:
			newItem.append(i.get())
		self.dataManager.addGameItem(newItem)
		self.window.destroy()
		messagebox.showinfo("Success", "Game is successfully saved!")

	def removeGames(self):
		""" Open window with remove item form. """
		self.window = Tk()
		self.window.title("Remove games")
		self.window.geometry('350x450')
		Label(self.window, text = "Select itemes", font=("Arial Bold", 15)).pack()
		self.gameList = self.createListBox(self.window, MULTIPLE)
		self.gameList.pack()
		Button(self.window, text="Remove selected", font=("Arial Bold", 12), width = 20, command = self.removeSelected).pack()
		self.window.mainloop()

	def removeSelected(self):
		""" Remove selected game from data file. """
		if len(self.gameList.curselection()) < 1:
			return
		for i in self.gameList.curselection():
			del self.dataManager.data[i]
		self.dataManager.updateDataFile()
		self.window.destroy()
		messagebox.showinfo("Success", "Selected games were successfully removed!")

	def editGames(self):
		""" Open window with edit item form. """
		self.window = Tk()
		self.window.title("Edit games")
		self.window.geometry('350x450')
		Label(self.window, text = "Select item", font=("Arial Bold", 15)).pack()
		self.gameList = self.createListBox(self.window, BROWSE)
		self.gameList.pack()
		Button(self.window, text="Edit selected", font=("Arial Bold", 12), width = 20, command = self.editSelected).pack()
		self.window.mainloop()

	def editSelected(self):
		""" Edit selected game. """
		if len(self.gameList.curselection()) < 1:
			return
		self.selectedEditIndex = self.gameList.curselection()[0]
		self.editWindow = Tk()
		self.editWindow.title("Edit game")
		self.editWindow.geometry('910x180')
		self.editWindow.grid()
		Label(self.editWindow, text = "Edit item", font=("Arial Bold", 15)).grid(row = 0, columnspan=len(self.dataManager.nameRow), pady= 8)
		c = 0
		for i in self.dataManager.nameRow:
			Label(self.editWindow, text = i, padx=7, borderwidth=2, relief="groove", font=("Arial", 12)).grid(row=1, column=c)
			c+=1
		self.newGameName = Entry(self.editWindow,width=15)
		self.newGameName.insert(0, self.dataManager.data[self.selectedEditIndex][0])
		self.newGameName.grid(row = 2, column = 0)
		self.combobox = []
		for i in range(1, len(self.dataManager.nameRow)):
			com = ttk.Combobox(self.editWindow, width = 3)
			com['values'] = (1, 2, 3, 4, 5)
			com.current(int(self.dataManager.data[self.selectedEditIndex][i]) - 1)
			com.grid(row=2, column = i)
			self.combobox.append(com)
		Button(self.editWindow, text = "Save", font=("Arial Bold", 12), width = 20, command = self.saveChanges).grid(row = 3, columnspan=len(self.dataManager.nameRow), pady= 15)
		self.editWindow.mainloop()

	def saveChanges(self):
		""" Save changes to data file. """
		if len(self.newGameName.get()) < 1:
			return
		self.dataManager.data[self.selectedEditIndex][0] = self.newGameName.get()
		j = 1
		for i in self.combobox:
			self.dataManager.data[self.selectedEditIndex][j] = i.get()
			j+=1
		self.dataManager.updateDataFile()
		self.editWindow.destroy()
		self.window.attributes("-topmost", True)
		messagebox.showinfo("Success", "Game is successfully updated!")

	def submit(self):
		""" Action on 'Advise' button. """
		self.answerBuilder.clearTypes()
		for i in self.gameTypesCheckDict:
			if self.gameTypesCheckDict[i].get():
				self.answerBuilder.addType(i)
		if self.answerBuilder.isNotEmptyAnswer():
			self.answer.delete(1.0, END)
			self.answer.insert(INSERT, self.answerBuilder.getAnswer(self.dataManager, self.radioSelected.get()))
		else:
			messagebox.showinfo("Warning", "No game types selected!")

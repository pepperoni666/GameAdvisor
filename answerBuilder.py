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

	def getAnswer(self, dataManager, flag):
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
			addRow = True
			for i in range(1, len(row)):
				if i in typesNums:
					if flag == "and":
						if int(row[i]) is 1:
							addRow = False
					p+=int(row[i])
			if addRow:
				top[row[0]] = p
		top_sorted_values = sorted(top.items(), key=lambda kv: kv[1], reverse=True)
		result = ""
		for i in range(0, len(top_sorted_values)):
			if top_sorted_values[i][1] is len(typesNums):
				break
			result += str(i+1) + ". " + top_sorted_values[i][0] + "\t\t\t\t\t(" + str(top_sorted_values[i][1]) + "p)" + "\n"
		return result

class Shift:
	def __init__(self, date, start_t, end_t, position="Front End"):
		self.date = date
		self.start_t = start_t
		self.end_t = end_t
		self.position = position

	def __str__(self):
		return self.date + " Start Time: " + self.start_t + " End Time: " + self.end_t

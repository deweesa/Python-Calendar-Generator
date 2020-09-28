class Shift:
	def __init__(self, date, start_t, end_t, position=None):
		self.date = self.__toRFCDate(date)
		self.start_t = self.__toRFCTime(start_t) 
		self.end_t = self.__toRFCTime(end_t)
		self.position = position
		if self.position is not None:
			if len(self.position.split("/")) == 2:
				self.position = self.position.split("/")[1]
			else:
				self.position = None

	def __toRFCTime(self, time):
		time_comps = time.split()
		period = time_comps[1]	
		hour = time_comps[0].split(':')[0]
		if(period == 'PM'):
			hour = 12 + (int(hour)%12) 
			hour = str(hour)
		elif(len(hour) != 2):
			hour = '0' + hour

		minute = time_comps[0].split(':')[1]
		return hour + ':' + minute + ':00-07:00'
		
	def __toRFCDate(self, date):
		date_comps = date.split('/')

		year = date_comps[2]

		month = date_comps[0]
		if len(month) != 2:
			month = '0' + month

		day = date_comps[1]
		if len(day) != 2:
			day = '0' + day
		
		return year + '-' + month + '-' + day

	def __str__(self):
		result =  self.date + " Start Time: " + self.start_t + " End Time: " + self.end_t 
		if self.position is not None:
			result = self.position + ' ' + result
		return result

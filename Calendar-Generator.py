import PyPDF2

def main():
	sched_txt = getScheduleText() 
	parseSchedule(sched_txt)

def getScheduleText():
	pdfFileObj = open('schedule.pdf', 'rb')
	pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
	pageObj = pdfReader.getPage(0)
	return pageObj.extractText()  

def parseSchedule(schedule):
	day_helper = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]    
	for day in day_helper:
		print(day)
		slice_start = schedule.find(day)+len(day)
#		print(schedule[slice_start:])
		contents = schedule[slice_start:].split("\n");
		print(contents[:8])
		
		work_day = False
		for piece in contents[:3]:
			if 'AM' or 'PM' in piece:
				print(piece + "yo it true")
				work_day = True	
		if work_day is True:
			print(day + " Is a work Day")
		
		print("\n")

if __name__ =="__main__":
	main()

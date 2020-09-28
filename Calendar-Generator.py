from __future__ import print_function
from Shift import Shift
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import googleapiclient.errors
import PyPDF2
import datetime
import pickle
import os.path
import json
import sys
# secrets holds the calendarIds of my Work calendar 
# and calendar used for testing, figure it shouldn't be on github
from secrets import  WORK, TEST, PATH 

SCOPES = ['https://www.googleapis.com/auth/calendar']
#PRIM = 'primary'

def main():
	#Might want to change to getopt, instead of naive flag check. 
	if len(sys.argv) > 1:
		if sys.argv[1] in ['-d', '--debug']:
			debug = True
			calendar = TEST
	else:
		debug = False
		calendar = WORK

	service = getService()

	if not debug:
		files = os.listdir(PATH)
		for f in files:
			sched_txt = getScheduleText(os.path.join(PATH, f))
			work_week = parseSchedule(sched_txt)
			printShifts(work_week)
			addShiftsToCalen(service, work_week, calendar)
			#os.remove(os.path.join(PATH, f))

	else:
		#		printShifts(work_week)
		files = os.listdir(PATH)
		for f in files:
			sched_txt = getScheduleText(os.path.join(PATH, f))
			work_week = parseSchedule(sched_txt)
			printShifts(work_week)
			addShiftsToCalen(service, work_week, calendar)

def getScheduleText(path):
	pdfFileObj = open(path, 'rb')
	pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
	pageObj = pdfReader.getPage(0)
	return pageObj.extractText()  

def parseSchedule(schedule):
	day_helper = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]    
	work_week = []
	for day in day_helper:
#		print(day)
		slice_start = schedule.find(day)+len(day)
		contents = schedule[slice_start:].split("\n");
#		print(contents[:8])
		
		work_day = False
		for piece in contents[:3]:
			if "AM" in piece or "PM" in piece:
				work_day = True	
		if work_day is True:
#			print(day + " Is a work Day")
			work_week.append(Shift(contents[1], contents[2], contents[3], contents[6]))
#			print(contents[3])
			
		
#		print("\n")
#	for day in work_week:
#		print(day)

	return work_week

def getService():
	creds = None

	if os.path.exists('token.pickle'):
		with open('token.pickle', 'rb') as token:
			creds = pickle.load(token)
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
			creds = flow.run_local_server(port=0)
		with open('token.pickle', 'wb') as token:
			pickle.dump(creds, token)

	service = build('calendar', 'v3', credentials=creds)
	return service

def addShiftsToCalen(service, work_week, calendar):
	f = open('eventTemplate.json')

	event_template = json.load(f)
	for day in work_week:
		work = "Work"
		if day.position is not None:
			work += " - " + day.position
		event = {
			'summary': work,
			'start': {
				'dateTime': day.date+'T'+day.start_t,
				'timeZone': 'America/Los_Angeles',
			},
			'end': {
				'dateTime': day.date+'T'+day.end_t,
				'timeZone': 'America/Los_Angeles',
			}
		}	
		
		try:		
			event = service.events().insert(calendarId=calendar, body=event).execute()
		except googleapiclient.errors.HttpError as err:
			print(err)

def printShifts(work_week):
	for day in work_week:
		print(day)

def testingStuff(service):
	event = {
		'summary': 'test',
		'description': 'testing testing testing',
		'start': {
			'dateTime': '2020-09-14T15:00:00-07:00',
			'timeZone': 'America/Los_Angeles',
		},
		'end': {
			'dateTime': '2020-09-14T18:00:00-07:00',
			'timeZone': 'America/Los_Angeles',
		}
	}
	
	event = service.events().insert(calendarId=TEST, body=event).execute()
	print("Event created")

def scanDirectory():
	files = os.listdir(PATH)
	
	for f in files:
		print(f)
	
	os.remove(os.path.join(PATH, 'test.txt'))

if __name__ =="__main__":
	main()

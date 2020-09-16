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
# secrets holds the calendarIds of my Work calendar 
# and calendar used for testing, figure it shouldn't be on github
from secrets import  WORK, TEST 

SCOPES = ['https://www.googleapis.com/auth/calendar']
#PRIM = 'primary'

def main():
	sched_txt = getScheduleText() 
	work_week = parseSchedule(sched_txt)
	service = getService()
	addShiftsToCalen(service, work_week)

def getScheduleText():
	pdfFileObj = open('schedule21.pdf', 'rb')
	pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
	pageObj = pdfReader.getPage(0)
	return pageObj.extractText()  

def parseSchedule(schedule):
	day_helper = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]    
	work_week = []
	for day in day_helper:
		print(day)
		slice_start = schedule.find(day)+len(day)
#		print(schedule[slice_start:])
		contents = schedule[slice_start:].split("\n");
		print(contents[:8])
		
		work_day = False
		for piece in contents[:3]:
			if "AM" in piece or "PM" in piece:
				#print(piece + "yo it true")
				#print(type(piece))
				work_day = True	
		if work_day is True:
			print(day + " Is a work Day")
#	!!!Deprecated - Going to change the order of Shift creation and converting from shift date/time to rfc date/time
			work_week.append(Shift(contents[1], contents[2], contents[3]))
			print(contents[3])
			
		
		print("\n")
	for day in work_week:
		print(day)

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
#	now = datetime.datetime.utcnow().isoformat() + 'Z'
#	print('Getting the upcoming 10 events')
#	events_result = service.events().list(calendarId=WORK, timeMin=now, maxResults=10, singleEvents = True, orderBy='startTime').execute()
#	events = events_result.get('items', [])
	#print(service.calendars.get())

#	if not events:
#		print('No upcoming events found.')
#	for event in events:
#		start = event['start'].get('datetime', event['start'].get('date'))
#		print(start, event['summary'])

def addShiftsToCalen(service, work_week):
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
			event = service.events().insert(calendarId=WORK, body=event).execute()
		except googleapiclient.errors.HttpError as err:
			print(err)

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

if __name__ =="__main__":
	main()

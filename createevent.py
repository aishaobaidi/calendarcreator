from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http 
from oauth2client import file, client, tools

try:
	import argparse
	flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
	flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
	flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
	creds = tools.run_flow(flow, store, flags) \
	        if flags else tools.run(flow, store)
CAL = build('calendar', 'v3', http=creds.authorize(Http()))

GMT_OFF = '+01:00'		# PDT/MST/GMT
EVENT = {
	'summary': 'paintball',
	'start':  {'dateTime': '2017-09-09T09:00:00%s' % GMT_OFF},
	'end':    {'dateTime': '2017-09-09T16:00:00%s' % GMT_OFF},
	'attendees': [
		{'email': '***@gmail.com'}
		],
}

e = CAL.events().insert(calendarId='primary',
	sendNotifications=True, body=EVENT).execute()

print('''*** %r event added:
	Start: %s
	End:   %s''' % (e['summary'].encode('utf-8'),
		e['start']['dateTime'], e['end']['dateTime']))
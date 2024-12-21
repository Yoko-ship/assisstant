from google.oauth2 import service_account
from googleapiclient.discovery import build


class GoogleCalendar:
    
  scopes = ["https://www.googleapis.com/auth/calendar"]
  file_path = "gen-lang-client-0844653717-4105bf824b66.json"
  def __init__(self):
    self.calendar_id = "ba4966183@gmail.com"
    creditentals = service_account.Credentials.from_service_account_file(filename=self.file_path, scopes=self.scopes)
    self.service = build("calendar","v3",credentials=creditentals)

  def get_calendar(self):
    return self.service.calendarList().list().execute()
  
  def create_calendar(self):
    calendar_list_entry = {
    'id': self.calendar_id
    }
    return self.service.calendarList().insert(body=calendar_list_entry).execute()
  
  def add_events(self,summary,description,startTime,endTime,timeZone):
    event = {
      'summary': summary,
      'description': description,
      'start': {
          'dateTime': startTime,
          'timeZone': timeZone
      },
      'end': {
        'dateTime': endTime,
        'timeZone': timeZone
      },
    }

    event = self.service.events().insert(calendarId=self.calendar_id, body=event).execute()
    return event["id"]
  def remove_events(self,id):
    self.service.events().delete(calendarId=self.calendar_id, eventId=id).execute()
    print("Напоминания успешно удалилась")
from __future__ import print_function
from flask import Flask, request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']
app = Flask(__name__)


@app.route("/")
def index():
    return "Need Json data to create calendar event"

#Approute here needs to be whatever is sending the request, I'm not sure where it's coming from.
@app.route('/postjson', methods=['POST','GET'])
def main():
    content = request.get_json()
    print(content)
    creds = None
    # The file token.json stores the user's access and refresh tokens, and isç
    # created automatically when the authorization flow completes for the first
    # time.
    # If there are no (valid) credentials available, let the user log in.
    if not creds:
        flow = InstalledAppFlow.from_client_secrets_file(
            'client_secret_117516734307-m218uj61m7b7i3dkplrpaoqaptpttbpb.apps.googleusercontent.com.json', SCOPES)
        creds = flow.run_local_server(port=8080)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('calendar', 'v3', credentials=creds)
        event = {
            'summary':  content["title"],
            'description': content["description"],
            'location': content["video_link"],  # Google Link meeting
            'start': {
                'dateTime': content["start_date"],  # Real date Time - HAS TO BE IN FORMAT "2022-04-28T17:00:00"
                'timeZone': 'America/New_York', # If There is no timeZone, dateTime format needs an offset
            },
            'end': {
                'dateTime': content["end_date"],
                'timeZone': 'America/New_York',
            },
            'attendees': [
                {'email': content["sender_email"]},  # The emails need to be part of Test Users under Oauth Consent.
                {'email': content["recipient_email"]}
            ],
        }
        event = service.events().insert(calendarId='primary', sendUpdates="all", body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))
    except HttpError as error:
        print('An error occurred: %s' % error)

    return content


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


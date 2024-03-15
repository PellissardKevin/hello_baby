#!/usr/bin/env python3

import kivy
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import Screen

import webbrowser

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

Window.size = (430, 932)

kivy.require('2.0.0')

class Appointement(Screen):
    def __init__(self, **kwargs):
        super(Appointement, self).__init__(**kwargs)

    def calendarAPI(self):
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        creds = None

        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "client_secret_2.json",
                    SCOPES,
                    redirect_uri='https://hello-baby.fr'
                )
                creds = flow.run_local_server(port=0)

                # Save the credentials for the next run
                with open("token.json", "w") as token:
                    token.write(creds.to_json())

        try:
            service = build("calendar", "v3", developerKey=hello_baby_api.config.google_key)

            # Call the Calendar API
            now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
            print("Getting the upcoming 10 events")
            events_result = (
                service.events()
                .list(
                    calendarId="primary",
                    timeMin=now,
                    maxResults=10,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = events_result.get("items", [])

            if not events:
                print("No upcoming events found.")
                return

            # Prints the start and name of the next 10 events
            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                print(start, event["summary"])

        except HttpError as error:
            print(f"An error occurred: {error}")

            events_text = ""
            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                events_text += f"{start}: {event['summary']}\n"

            # Mettez à jour le texte du Label avec les détails des événements
            self.ids.events_label.text = events_text

            auth_url = flow.authorization_url[0]

            # Open the authorization URL automatically in the default browser
            webbrowser.open(auth_url)

    def url_doctolib(self):
        webbrowser.open("https://www.doctolib.fr/")


class appointementfile(App):
    def build(self):
        return Appointement()

if __name__ == '__main__':
    appointementfile().run()


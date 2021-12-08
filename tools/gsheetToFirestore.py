# google sheet imports
from __future__ import print_function
import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# Firebase Imports
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of the registration spreadsheet
REGISTRATION_SHEET_ID = '1TXYp6vhDVhiGli1m3Pd_WHVYn7-3wwK9Me8T6FBENAA'
REGISTRATION_RANG_RFID = 'Y2021-2022-Roster!A2:D'

class SheetToFirestore():
    Season = "Season2021-2022"
    History = "History"
    AttnHistory = "AttnHistory"

    def __init__(self) -> None:
        # Firestore setup
        self.fcred = credentials.Certificate(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))
        firebase_admin.initialize_app(self.fcred)
        self.db = firestore.client()

        # google sheet API setup
        self.gscreds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.gscreds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.gscreds or not self.gscreds.valid:
            if self.gscreds and self.gscreds.expired and self.gscreds.refresh_token:
                self.gscreds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.gscreds = flow.run_local_server(port=61232)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(self.gscreds, token)

        self.service = build('sheets', 'v4', credentials=self.gscreds)
        self.index = 2
        self.rfidtag = 'A'
        self.name = 'B'

    def createFirestore(self):
        # open the google sheet and read each row

        # Call the Sheets API
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=REGISTRATION_SHEET_ID,
                                    range=REGISTRATION_RANG_RFID).execute()
        values = result.get('values', [])

        if values:
            print('RFID, Last, First:')
            seaon_collection = self.db.collection(self.Season)
            for row in values:
                # Print columns A and E, which correspond to indices 0 and 4.
                print('%s, %s, %s' % (row[2], row[0], row[1]))
                rfid_ref = seaon_collection.document(row[2])
                rfid_ref.collection(self.AttnHistory).document(self.History).set({})
                rfid_ref.set({
                     u'First' : row[1],
                     u'Last' : row[0],
                     u"RFIDTag" : row[2]
                })
        else:
            print("No data found!")

if __name__ == "__main__":
    sheetToFirestore = SheetToFirestore()
    sheetToFirestore.createFirestore()



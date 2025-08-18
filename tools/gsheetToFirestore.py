# google sheet imports
from __future__ import print_function
import os
import pickle
import argparse
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
# Firebase Imports
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of the registration spreadsheet
REGISTRATION_RANG_RFID = 'Registration!A2:D'

class SheetToFirestore():
    Season = None
    SheetId = None
    RFIDS = "members/rfids"

    def __init__(self, season, sheetId) -> None:
        self.Season = season
        self.SheetId = sheetId
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
        self.name = 'A' 
        self.rfidtag = 'B'
        self.role = 'C'

    def createFirestore(self):
        # open the google sheet and read each row

        try:
            # Call the Sheets API
            sheet = self.service.spreadsheets()
            result = sheet.values().get(spreadsheetId=self.SheetId,
                                        range=REGISTRATION_RANG_RFID).execute()
            values = result.get('values', [])

            if values:
                print('RFID, Last, First:, Role:')
                seaon_collection = self.db.collection(self.Season + '/' + self.RFIDS)
                for row in values:
                    # Print columns A and E, which correspond to indices 0 and 4.
                    print('%s, %s, %s, %s' % (row[2], row[0], row[1], row[3]))
                    rfid_ref = seaon_collection.document(row[2])
                    rfid_ref.set({})
                    rfid_ref.set({
                        u'First' : row[0],
                        u'Last' : row[1],
                        u"RFIDTag" : row[2],
                        u"Role" : row[3],
                        u"attendanceCount" : 0
                    })
            else:
                print("No data found!")
        except HttpError as err:
            print(err)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="gsheetToFirestore", 
        description="Importing Attendance into database from Google sheet")
    parser.add_argument('-s', '--season')
    parser.add_argument('-sid', '--sheetId')

    args = parser.parse_args()
    sheetToFirestore = SheetToFirestore(args.season, args.sheetId)
    sheetToFirestore.createFirestore()



# Attendant
This repository contains the python attendant application for FRC Team 151. This application requires the Raspberry Pi Model 3 and a HID RFID reader. This application stores the attendant history in Google Firebase. A Firebase project is required and a firestore data is required for storing attendant data.

## To install dependencies

- Install Python3
- Install the Python pre-requisites using the requirements.txt

```
pip3 install -r requirements.txt
```

## To run the App

Open a console, and change directory to the root directory of the source tree. Run the following command. The -s specifies the season property. Typical season property is SeasonYYYY-YYYY where the first YYYY specified the current year and the second YYYY specified the following year.

```
python3 AttendantMain.py -s Season2025-2026
```
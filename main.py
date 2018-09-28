import httplib2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow
from googleapiclient.discovery import build
import matplotlib.pyplot as plt;

plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

CLIENT_SECRET = ".\\client_secret.json"
SCOPE = 'https://www.googleapis.com/auth/spreadsheets.readonly'
STORAGE = Storage('credentials.storage')


# Start the OAuth flow to retrieve credentials


def authorize_credentials():
    # Fetch credentials from storage
    credentials = STORAGE.get()
    # If the credentials doesn't exist in the storage location then run the flow
    if credentials is None or credentials.invalid:
        flow = flow_from_clientsecrets(CLIENT_SECRET, scope=SCOPE)
        http = httplib2.Http()
        credentials = run_flow(flow, STORAGE, http=http)
    return credentials


def get_google_sheet(spreadsheetId):
    credentials = authorize_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
    service = build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)

    rangeName = "Responses Copy"
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])
    return values


def makeGraph(spreadsheetId):
    get_google_sheet(spreadsheetId)


def main():
    values = get_google_sheet('1Jh3ehawbeYeLSsCBQFuO_MKqE6IjBDBByY6qBvC7K-k')

    # print("Timestamp\t\t\tStudent\t\tClass\t\tTest\t\tGrade Guesss\tMethod(s) Used\tMethod(s) Future")

    ids = []
    strategies = []
    grades = []
    for value in range(len(values)):
        ids.append(values[value][2])
        strategies.append(values[value][5])
        grades.append(values[value][10])
        print()


if __name__ == main():
    main()

import xlrd
import httplib2
from flask import flash
from googleapiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client.tools import run_flow
import gspread

CLIENT_SECRET = ".\\client_secret.json"
SCOPE = 'https://www.googleapis.com/auth/spreadsheets'
STORAGE = Storage('credentials.storage')
spreadsheet_id = '1Jh3ehawbeYeLSsCBQFuO_MKqE6IjBDBByY6qBvC7K-k'


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


def get_google_sheet(range_name):
    credentials = authorize_credentials()
    http = credentials.authorize(httplib2.Http())
    discovery_url = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
    service = build('sheets', 'v4', http=http, discoveryServiceUrl=discovery_url)
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])
    return values


def verify(filename, exam, class_num):
    gsheet = get_google_sheet("Responses Copy")
    loc = ".//upload//"+filename
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)
    found = []
    ids = []
    count = 0

    for i in range(sheet.nrows):
        student_id = sheet.cell_value(i, 0)
        if isinstance(student_id, float):
            student_id = str(sheet.cell_value(i, 0))
            ids.append(student_id[:-2])
        else:
            ids.append(student_id.upper())

    for i in range(len(gsheet)):
        if gsheet[i][3] == exam and gsheet[i][2] == class_num and gsheet[i][1].upper() in ids:
            found.append([])
            found[len(found) - 1].append(gsheet[i][1].upper())
            found[len(found)-1].append(i)

    for i in range(len(ids)):
        for j in range(len(found)):
            if found[j][0] == ids[i]:
                found[j].append(sheet.cell_value(i, 1))
                print("Found student #" + found[j][0] + " at row " +
                      str(i+1) + " with grade " + str(int(sheet.cell_value(i, 1))))
                count = count + 1
    print(found)
    print(len(found))
    if count == 0:
        flash("Nothing to add", 'cat1')
    else:
        flash(str(count) + " students out of " + str(len(found)) + " found", 'cat2')
        return found


def upload(result):
    print(result)

    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    gc = gspread.authorize(credentials)
    sheet = gc.open("Study strategies (Responses)").get_worksheet(1)
    for i in range(len(result)):
        if result[i][2]:
            print("inserting at row: " + str((result[i][1]+1)))
            sheet.update_cell(result[i][1]+1, 12, result[i][2])
    """
    credentials = authorize_credentials()
    http = credentials.authorize(httplib2.Http())
    discovery_url = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
    service = build('sheets', 'v4', http=http, discoveryServiceUrl=discovery_url)
    rangeName = "Test!A1:A5"
    values = [
        [
            500, 400, 300, 200, 100,
        ],
    ]
    Body = {
        'values': values,
        'majorDimension': 'COLUMNS',
    }
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=rangeName,
        valueInputOption='USER_ENTERED', body=Body).execute()
"""
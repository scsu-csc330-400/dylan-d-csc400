import httplib2
import numpy as np
from googleapiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow
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


def get_google_sheet(spreadsheet_id, range):
    credentials = authorize_credentials()
    http = credentials.authorize(httplib2.Http())
    discovery_url = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
    service = build('sheets', 'v4', http=http, discoveryServiceUrl=discovery_url)
    range_name = range
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])
    return values


def main():
    values = get_google_sheet('1Jh3ehawbeYeLSsCBQFuO_MKqE6IjBDBByY6qBvC7K-k', "Responses Copy")
    strats = get_google_sheet('1Jh3ehawbeYeLSsCBQFuO_MKqE6IjBDBByY6qBvC7K-k', "Lookup!A13:C28")

    colors = []
    strat_strings = []

    for i in range(len(strats)):
        strat_strings.append(strats[i][0])
        if strats[i][2] == "P":
            colors.append("red")
        elif strats[i][2] == "A":
            colors.append("blue")

    avgs = [0] * 13
    sum_strats = [0] * 17
    sums = [0] * 17
    class_num = "101"

    for i in range(len(values)):
        if values[i][2] == class_num:
            tmp = values[i][5].split(",")
            for j in range(len(tmp)):
                if tmp[j] != "":
                    sum_strats[int(tmp[j])] = sum_strats[int(tmp[j])] + 1
                    sums[(int(tmp[j]))] = sums[(int(tmp[j]))] + int(values[i][10])

    sum_strats.pop(0)
    sums.pop(0)
    sum_strats.pop(3)
    sums.pop(3)
    sum_strats.pop(10)
    sums.pop(10)
    sum_strats.pop(13)
    sums.pop(13)
    print(sum_strats)
    print(sums)

    for i in range(len(sum_strats)):
        if sums[i] == 0:
            avgs[i] = 0
        else:
            avgs[i] = int(sums[i] / sum_strats[i])

    print(avgs)

    avgs, strat_strings = (list(t) for t in zip(*sorted(zip(avgs, strat_strings))))
    print(avgs)

    for i in range(len(avgs)):
        if avgs[0] == 0:
            avgs.pop(0)
            strat_strings.pop(0)

    index = np.arange(len(strat_strings))
    plt.bar(index, avgs, align='edge', color=['blue', 'red', 'red', 'blue', 'red', 'red'])
    plt.xlabel('Study Strategies', fontsize=15)
    plt.ylabel('Averages', fontsize=15)
    plt.xticks(index, strat_strings, fontsize=8, rotation=30)
    plt.title('BIO ' + class_num + ' Exam #1', fontsize=20)
    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.25, top=0.95)
    figure = plt.gcf()
    figure.set_size_inches(20, 9)
    figure.savefig('BIO ' + class_num + '.png', dpi=150)


if __name__ == main():
    main()

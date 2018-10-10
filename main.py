import textwrap

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


def get_google_sheet(spreadsheet_id, range_name):
    credentials = authorize_credentials()
    http = credentials.authorize(httplib2.Http())
    discovery_url = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
    service = build('sheets', 'v4', http=http, discoveryServiceUrl=discovery_url)
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])
    return values


def main():
    values = get_google_sheet('1Jh3ehawbeYeLSsCBQFuO_MKqE6IjBDBByY6qBvC7K-k', "Responses Copy")
    strats = get_google_sheet('1Jh3ehawbeYeLSsCBQFuO_MKqE6IjBDBByY6qBvC7K-k', "Lookup!A13:C28")

    class_num = "200"

    colors = []
    strat_strings = []

    for i in range(len(strats)):
        if strats[i][2] == "P":
            colors.append("red")
        elif strats[i][2] == "A":
            colors.append("blue")

    avgs = [0] * len(colors)
    tmp_sum_strats = [0] * (len(strats))
    tmp_sums = [0] * (len(strats))

    for i in range(len(values)):
        if values[i][2] == class_num:
            tmp = values[i][5].split(",")
            for j in range(len(tmp)):
                if tmp[j] != "":
                    tmp_sum_strats[int(tmp[j])] = tmp_sum_strats[int(tmp[j])] + 1
                    tmp_sums[(int(tmp[j]))] = tmp_sums[(int(tmp[j]))] + int(values[i][10])

    print(tmp_sum_strats)
    print(tmp_sums)

    sum_strats = []
    sums = []

    for i in range(len(tmp_sum_strats)):
        if strats[i][2] != "N/A":
            sum_strats.append(tmp_sum_strats[i])
            sums.append(tmp_sums[i])
            strat_strings.append(strats[i][0])

    print(sum_strats)
    print(sums)

    for i in range(len(sum_strats)):
        if sums[i] == 0:
            avgs[i] = 0
        else:
            avgs[i] = int(sums[i] / sum_strats[i])

    avgs, strat_strings, colors = (list(t) for t in zip(*sorted(zip(avgs, strat_strings, colors))))
    print(avgs)

    for i in range(len(avgs)):
        if avgs[0] == 0:
            avgs.pop(0)
            strat_strings.pop(0)
            colors.pop(0)

    strat_strings = [textwrap.fill(text, 15) for text in strat_strings]

    index = np.arange(len(strat_strings))
    plt.bar(index, avgs, align='center', color=colors)
    plt.xlabel('Study Strategies', fontsize=15)
    plt.ylabel('Averages', fontsize=15)
    plt.xticks(index, strat_strings, fontsize=10)
    plt.title('BIO ' + class_num + ' Exam #1', fontsize=20)
    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.20, top=0.95)
    figure = plt.gcf()
    figure.set_size_inches(20, 8)
    figure.savefig('BIO ' + class_num + '.png', dpi=150)


main()

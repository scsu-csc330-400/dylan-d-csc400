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


def get_google_sheet(spreadsheet_id):
    credentials = authorize_credentials()
    http = credentials.authorize(httplib2.Http())
    discovery_url = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
    service = build('sheets', 'v4', http=http, discoveryServiceUrl=discovery_url)
    range_name = "Responses Copy"
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])
    return values


def make_graph(spreadsheet_id):
    get_google_sheet(spreadsheet_id)


def main():
    values = get_google_sheet('1Jh3ehawbeYeLSsCBQFuO_MKqE6IjBDBByY6qBvC7K-k')

    # print("Timestamp\t\t\tStudent\t\tClass\t\tTest\t\tGrade Guesss\tMethod(s) Used\tMethod(s) Future")

    avgs = [0] * 13
    sum_strats = [0] * 17
    sums = [0] * 17
    strat_strings = ["I attended class",
                     "I paid attention in class",
                     "I participated in class",
                     # "None of the listed responses",
                     "Rereading chapters in the textbook",
                     "Highlighting material in\nthe textbook",
                     "Rereading class notes",
                     "Rewriting class notes (verbatim) ",
                     "Rewriting class notes (while\nactively reorganizing material)",
                     "Rereading class learning\nobjectives or goals",
                     "Using class learning objectives\nor goals as practice exam questions",
                     # "Studying independently",
                     "Creating and using flashcards",
                     "Quizzing myself with a blank sheet\nof paper or dry erase board",
                     # "Studying with a classmate or in small groups",
                     "Asking questions in office hours"
                     ]

    for i in range(len(values)):
        if values[i][2] == "200":
            tmp = values[i][5].split(",")
            for j in range(len(tmp)):
                if tmp[j] != "":
                    sum_strats[int(tmp[j])] = sum_strats[int(tmp[j])] + 1
                    sums[(int(tmp[j]))] = sums[(int(tmp[j]))] + int(values[i][10])

    print(sum_strats)
    print(sums)
    sum_strats.pop(0)
    sums.pop(0)
    sum_strats.pop(3)
    sums.pop(3)
    sum_strats.pop(10)
    sums.pop(10)
    sum_strats.pop(13)
    sums.pop(13)

    for i in range(len(sum_strats)):
        if sums[i] == 0:
            avgs[i] = 0
        else:
            avgs[i] = int(sums[i] / sum_strats[i])

    print(avgs)

    index = np.arange(len(strat_strings))
    plt.bar(index, avgs, align='edge', color=['red', 'blue', 'blue', 'red', 'red', 'red', 'red',
                                              'blue', 'red', 'blue', 'blue', 'blue', 'blue'])
    plt.xlabel('Study Strategies', fontsize=15)
    plt.ylabel('Averages', fontsize=15)
    plt.xticks(index, strat_strings, fontsize=8, rotation=30)
    plt.title('Exam #1', fontsize=20)
    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.25, top=0.95)
    figure = plt.gcf()
    figure.set_size_inches(20, 8)
    figure.savefig('foo.png', dpi=150)


if __name__ == main():
    main()

import textwrap
import numpy as np
import sheet

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def make_graph(exam, class_num, color_passive, color_active):
    values = sheet.get_google_sheet("Responses Copy")
    strats = sheet.get_google_sheet("Lookup!A13:28")
    colors = []
    strat_strings = []
    sum_strats = []
    sums = []

    for i in range(len(strats)):
        if strats[i][2] == "P":
            colors.append(color_passive)
        elif strats[i][2] == "A":
            colors.append(color_active)

    avgs = [0] * len(colors)
    tmp_sum_strats = [0] * (len(strats))
    tmp_sums = [0] * (len(strats))

    for i in range(len(values)):
        if values[i][2] == class_num and values[i][3] == exam:
            tmp = values[i][5].split(",")
            for j in range(len(tmp)):
                if tmp[j] != "":
                    tmp_sum_strats[int(tmp[j])] = tmp_sum_strats[int(tmp[j])] + 1
                    tmp_sums[(int(tmp[j]))] = tmp_sums[(int(tmp[j]))] + int(values[i][10])

    print(tmp_sum_strats)
    print(tmp_sums)

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
    plt.title('BIO ' + class_num + ' Exam #' + exam, fontsize=20)
    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.20, top=0.95)
    figure = plt.gcf()
    figure.set_size_inches(20, 8)
    figure.savefig('.//graphs//BIO ' + class_num + '.png', dpi=150)
    figure.clf()




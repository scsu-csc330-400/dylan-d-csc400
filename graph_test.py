import os
import textwrap
import numpy as np

import matplotlib
import six
from matplotlib import colors

import db

matplotlib.use('Agg')
import matplotlib.pyplot as plt


def test(exam, class_num, color_passive, color_active):
    conn = db.db_conn()

    avgs = []
    strats = []
    color = []
    cursor = conn.cursor()
    for i in range(13):
        query = (
            "SELECT SUM(grade) / COUNT(grade) AS avg1 FROM Responses INNER JOIN methods_used ON "
            "Responses.response_id = methods_used.methods_used_id WHERE (methods_used.`{}` = 1 AND "
            "Responses.exam_num = {} AND Responses.class_id = {})".format(i, exam, class_num))
        cursor.execute(query)
        result = cursor.fetchall()
        for j in result:
            if j[0] is not None:
                avgs.append(int(j[0]))
            else:
                avgs.append(0)
    print(avgs)

    for i in range(13):
        cursor.execute("SELECT method_name, type FROM Methods WHERE type <> 'N'")
        result = cursor.fetchall()
        for j in result:
            strats.append(j[0])
            if j[1] == "P":
                color.append(color_passive)
            else:
                color.append(color_active)

    avgs, strats, color_list = (list(t) for t in zip(*sorted(zip(avgs, strats, color))))

    for i in range(len(avgs)):
        if avgs[0] == 0:
            avgs.pop(0)
            strats.pop(0)
            color.pop(0)

    print(avgs)

    cursor.execute("SELECT CRN, class_name, class_num FROM Class Where class_id = {}".format(class_num))
    class_title = cursor.fetchall()
    CRN = class_title[0][0]
    class_name = class_title[0][1]
    class_num = class_title[0][2]

    strats = [textwrap.fill(text, 15) for text in strats]

    index = np.arange(len(strats))
    plt.bar(index, avgs, align='center', color=color_list)
    plt.xlabel('Study Strategies', fontsize=15)
    plt.ylabel('Averages', fontsize=15)
    plt.xticks(index, strats, fontsize=10)
    plt.title('{} {} {} Exam {}'.format(CRN, class_name, class_num, exam), fontsize=20)
    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.20, top=0.95)
    figure = plt.gcf()
    figure.set_size_inches(20, 8)
    filename = 'graphs/norm {} {} {}.png'.format(CRN, class_name, class_num)
    figure.savefig('.//static//graphs//norm {} {} {}.png'.format(CRN, class_name, class_num), dpi=150)
    figure.clf()

    cursor.close()
    return filename


def test1(class_num):
    conn = db.db_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT count(exam_id) from Exam WHERE class_id = {}".format(class_num))
    exam_count = cursor.fetchall()[0][0]
    exam_list = []

    for i in range(exam_count):
        responses_list = []
        for j in range(13):
            cursor.execute(
                'SELECT count(`{}`) from methods_used where `{}` = 1 and class_id = {} and exam_id = {}'.format(
                    j, j, class_num, i + 1))
            result = cursor.fetchall()
            responses_list.append(result[0][0])
        exam_list.append(responses_list)

    strats = get_strats()[0]
    strats = [textwrap.fill(text, 15) for text in strats]

    index = np.arange(len(strats))
    width = 0.27

    fig = plt.figure()
    ax = fig.add_subplot(111)
    rects_list = []
    for i in range(len(exam_list)):
        if i == 0:
            rects = ax.bar(index, exam_list[i], width, color='red', label='Exam {}'.format(i))
            rects_list.append(rects)
            autolabel(rects, ax)
            print(exam_list[i])
        elif i == 1:
            rects = ax.bar(index + width, exam_list[i], width, color='green', label='Exam {}'.format(i))
            rects_list.append(rects)
            autolabel(rects, ax)
            print(exam_list[i])
        else:
            rects = ax.bar(index + width * i, exam_list[i], width, color='blue', label='Exam {}'.format(i))
            rects_list.append(rects)
            autolabel(rects, ax)
            print(exam_list[i])

    cursor.execute("SELECT CRN, class_name, class_num FROM Class Where class_id = {}".format(class_num))
    class_title = cursor.fetchall()
    CRN = class_title[0][0]
    class_name = class_title[0][1]
    class_num = class_title[0][2]

    conn.close()
    cursor.close()

    ax.set_title('By Exam for {} {} {}'.format(CRN, class_name, class_num))
    ax.set_ylabel('Responses')
    ax.set_xlabel('Strategies')
    ax.set_xticks(index + width)
    ax.set_xticklabels(strats)
    ax.legend()
    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.20, top=0.95)
    figure = plt.gcf()
    figure.set_size_inches(20, 8)

    filename = 'graphs/exam {} {} {}.png'.format(CRN, class_name, class_num)
    figure.savefig('.//static//graphs//exam {} {} {}'.format(CRN, class_name, class_num), dpi=150)
    figure.clf()
    return filename


def test2(semester):
    conn = db.db_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT class_id FROM Exam WHERE semester = '{}'".format(semester))
    class_id_list = cursor.fetchall()
    cursor.execute("SELECT DISTINCT exam_num FROM Exam WHERE semester = '{}'".format(semester))
    exam_num_list = cursor.fetchall()
    class_list = []
    for i in range(len(class_id_list)):
        exam_list = []
        for j in range(len(exam_num_list)):
            response_list = []
            for k in range(13):
                cursor.execute(
                    'SELECT count(`{}`) from .methods_used where `{}` = 1 and class_id = {} and '
                    'exam_id = {}'.format(k, k, class_id_list[i][0], exam_num_list[j][0]))
                result = cursor.fetchall()
                response_list.append(result[0][0])
            exam_list.append(response_list)
        class_list.append(exam_list)

    sums = []
    for i in range(len(class_list)):
        tmp = [sum(x) for x in zip(*class_list[i])]
        sums.append(tmp)
    print(sums)

    conn.close()
    cursor.close()
    color_list = get_colors()

    strats = get_strats()[0]
    strats = [textwrap.fill(text, 15) for text in strats]

    index = np.arange(len(strats))
    width = 0.27

    fig = plt.figure()
    ax = fig.add_subplot(111)

    rects_list = []
    for i in range(len(sums)):
        if i == 0:
            rects = ax.bar(index, sums[i], width, color='red', label='Class {}'.format(i + 1))
            rects_list.append(rects)
            autolabel(rects, ax)
            print(sums[i])
        elif i == 1:
            rects = ax.bar(index + width, sums[i], width, color='green', label='Class {}'.format(i + 1))
            rects_list.append(rects)
            autolabel(rects, ax)
            print(sums[i])
        else:
            rects = ax.bar(index + width * i, sums[i], width, color='blue', label='Class {}'.format(i + 1))
            rects_list.append(rects)
            autolabel(rects, ax)
            print(sums[i])

    ax.set_title('By semester for {}'.format(semester))
    ax.set_ylabel('Responses')
    ax.set_xlabel('Strategies')
    ax.set_xticks(index + width)
    ax.set_xticklabels(strats)
    ax.legend()
    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.20, top=0.95)
    figure = plt.gcf()
    figure.set_size_inches(20, 8)

    filename = 'graphs/semester {}.png'.format(semester)
    figure.savefig('.//static//graphs//semester {}.png'.format(semester), dpi=150)
    figure.clf()
    # print(class_list)
    # print(sums)
    return filename


def autolabel(rects, ax):
    for rect in rects:
        h = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * h, '%d' % int(h),
                ha='center', va='bottom')


def get_strats(color_passive="red", color_active="blue"):
    conn = db.db_conn()
    cursor = conn.cursor()
    strats = []
    color = []
    cursor.execute("SELECT method_name, type FROM Methods")
    result = cursor.fetchall()
    for j in result:
        strats.append(j[0])
        if j[1] == "P":
            color.append(color_passive)
        elif j[1] == "a":
            color.append(color_active)
        else:
            color.append("k")
    return strats, color


def get_colors():
    colors_ = list(six.iteritems(colors.cnames))

    # Add the single letter colors.
    for name, rgb in six.iteritems(colors.ColorConverter.colors):
        hex_ = colors.rgb2hex(rgb)
        colors_.append((name, hex_))

    # Transform to hex color values.
    hex_ = [color[1] for color in colors_]
    # Get the rgb equivalent.
    rgb = [colors.hex2color(color) for color in hex_]
    # Get the hsv equivalent.
    hsv = [colors.rgb_to_hsv(color) for color in rgb]

    # Split the hsv values to sort.
    hue = [color[0] for color in hsv]
    sat = [color[1] for color in hsv]
    val = [color[2] for color in hsv]

    # Sort by hue, saturation and value.
    ind = np.lexsort((val, sat, hue))
    sorted_colors = [colors_[i] for i in ind]
    return sorted_colors

import os
import textwrap
import numpy as np
import mysql.connector

import matplotlib

import db

matplotlib.use('Agg')
import matplotlib.pyplot as plt


def get_strats(color_passive="red", color_active="blue"):
    conn = db.db_conn()
    cursor = conn.cursor()
    strats = []
    color = []
    cursor.execute("SELECT method_name, type FROM Methods WHERE type <> 'N'")
    result = cursor.fetchall()
    for j in result:
        strats.append(j[0])
        if j[1] == "P":
            color.append(color_passive)
        else:
            color.append(color_active)
    return strats, color


def test(exam, class_num, color_passive, color_active):
    path = './/static//graphs//norm BIO ' + str(class_num) + '.png'
    if os.path.isfile(path):
        filename = 'graphs/norm BIO ' + str(class_num) + '.png'
        return filename
    else:
        conn = db.db_conn()

        avgs = []
        strats = []
        color = []
        cursor = conn.cursor()
        for i in range(13):
            query = ("SELECT SUM(grade) / COUNT(grade) AS avg1 FROM StudyStrategies1.Responses INNER JOIN methods_used ON "
                "StudyStrategies1.Responses.response_id = methods_used.methods_used_id WHERE (methods_used.`{}` = 1 AND "
                "StudyStrategies1.Responses.exam_num = {} AND StudyStrategies1.Responses.class_id = {})".format(i, exam, class_num))
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

        avgs, strats, colors = (list(t) for t in zip(*sorted(zip(avgs, strats, color))))

        for i in range(len(avgs)):
            if avgs[0] == 0:
                avgs.pop(0)
                strats.pop(0)
                color.pop(0)

        print(avgs)

        strats = [textwrap.fill(text, 15) for text in strats]

        index = np.arange(len(strats))
        plt.bar(index, avgs, align='center', color=colors)
        plt.xlabel('Study Strategies', fontsize=15)
        plt.ylabel('Averages', fontsize=15)
        plt.xticks(index, strats, fontsize=10)
        plt.title('BIO ' + str(class_num) + ' Exam #' + str(exam), fontsize=20)
        plt.subplots_adjust(left=0.05, right=0.95, bottom=0.20, top=0.95)
        figure = plt.gcf()
        figure.set_size_inches(20, 8)
        filename = 'graphs/norm BIO ' + str(class_num) + '.png'
        figure.savefig('.//static//graphs//norm BIO ' + str(class_num) + '.png', dpi=150)
        figure.clf()

        cursor.close()
        return filename


def test1(class_num):
    path = './/static//graphs//exam BIO ' + str(class_num) + '.png'
    if os.path.isfile(path):
        filename = 'graphs/exam BIO ' + str(class_num) + '.png'
        return filename
    else:
        conn = db.db_conn()
        exam1 = []
        exam2 = []
        exam3 = []
        cursor = conn.cursor()
        cursor.execute('SELECT grade FROM StudyStrategies1.Responses where class_id = {}'.format(class_num))
        result = cursor.fetchall()
        grades = result

        for i in range(12):
            cursor.execute(
                'SELECT count(`{}`) from StudyStrategies1.methods_used where `{}` = 1 and class_id = {} and exam_id = 1'.format(
                    i, i, class_num))
            result = cursor.fetchall()
            exam1.append(result[0][0])

            cursor.execute(
                'SELECT count(`{}`) from StudyStrategies1.methods_used where `{}` = 1 and class_id = {} and exam_id = 2'.format(
                    i, i, class_num))
            result = cursor.fetchall()
            exam2.append(result[0][0])

            cursor.execute(
                'SELECT count(`{}`) from StudyStrategies1.methods_used where `{}` = 1 and class_id = {} and exam_id = 3'.format(
                    i, i, class_num))
            result = cursor.fetchall()
            exam3.append(result[0][0])

        print(exam1, exam2, exam3)

        conn.close()
        cursor.close()

        strats = get_strats()[0]
        strats = [textwrap.fill(text, 15) for text in strats]

        index = np.arange(len(strats))
        width = 0.27

        fig = plt.figure()
        ax = fig.add_subplot(111)
        rects1 = ax.bar(index, exam1, width, color='red', label='Exam 1')
        rects2 = ax.bar(index+width, exam2, width, color='green', label='Exam 2')
        rects3 = ax.bar(index+width*2, exam3, width, color='blue', label='Exam 3')

        ax.set_title('By Exam for Class ' + class_num)
        ax.set_ylabel('Responses')
        ax.set_xlabel('Strategies')
        ax.set_xticks(index+width)
        ax.set_xticklabels(strats)
        ax.legend()
        plt.subplots_adjust(left=0.05, right=0.95, bottom=0.20, top=0.95)
        figure = plt.gcf()
        figure.set_size_inches(20, 8)

        autolabel(rects1, ax)
        autolabel(rects2, ax)
        autolabel(rects3, ax)
        filename = 'graphs/exam BIO ' + str(class_num) + '.png'
        figure.savefig('.//static//graphs//exam BIO ' + str(class_num) + '.png', dpi=150)
        figure.clf()
        return filename


def test3(semester):
    return


def autolabel(rects, ax):
    for rect in rects:
        h = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * h, '%d' % int(h),
                ha='center', va='bottom')

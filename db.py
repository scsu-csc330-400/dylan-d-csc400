import mysql.connector


def db_conn():
    db = mysql.connector.connect(
            host="104.154.246.246",
            user="TESTUSER",
            passwd="yankees1",
            database="StudyStrategies1"
        )
    return db

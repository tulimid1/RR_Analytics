from pytube import YouTube
from datetime import datetime
import sqlite3
import pandas as pd
import re
import string


class ScrapeYouTubeVideoViews:

    url = ""
    title = ""
    n_views = []

    date_time_full = datetime.now()
    capture_date = int(
        str(date_time_full.year) + str(date_time_full.month) + str(date_time_full.day)
    )

    db_table_name = ""

    def __init__(self, video_url):
        self.url = video_url
        video_data = YouTube(self.url)
        self.title = video_data.title
        self.set_db_table_name()
        self.n_views = video_data.views

    def set_db_table_name(self):
        subStr = "[%s ]" % string.punctuation
        self.db_table_name = '_' + re.sub(subStr, "_", self.title)

    def addData2DataBase(self):
        conn = self.connect2database()
        cursor = conn.cursor()

        tableExists = self.determineIfTableExists(cursor)
        if not tableExists:
            cursor.execute(
                "CREATE TABLE "
                + self.db_table_name
                + " (capture_date integer, views integer)"
            )

        cursor.execute(
            "INSERT INTO " + self.db_table_name + " VALUES (?, ?)",
            (
                self.capture_date,
                self.n_views,
            ),
        )

        conn.commit()
        conn.close()

    def connect2database(self):
        return sqlite3.connect("YouTubeVideoData.db")

    def determineIfTableExists(self, cursor):
        listOfTables = cursor.execute(
            """SELECT name FROM sqlite_master WHERE type='table' AND name=?; """,
            (self.db_table_name,),
        ).fetchall()

        if listOfTables == []:
            return False
        else:
            return True

    def extractDataFromDataBase(self):
        conn = self.connect2database()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM " + self.db_table_name)
        df = self.data2pdDataFrame(cursor)
        return df

    def data2pdDataFrame(self, cursor):
        column_names = cursor.description
        result = [
            {column_names[index][0]: column for index, column in enumerate(value)}
            for value in cursor.fetchall()
        ]
        df = pd.DataFrame(result)
        df["capture_date"] = pd.to_datetime(df["capture_date"], format="%Y%m%d")
        df = df.set_index("capture_date")
        return df

    def __str__(self) -> str:
        date = datetime.strptime(str(self.capture_date), "%Y%m%d")
        month, day, year = date.month, date.day, date.year
        return f"Video: '{self.title}' has {self.n_views:.0f} views on {month}-{day}-{year}.\n"

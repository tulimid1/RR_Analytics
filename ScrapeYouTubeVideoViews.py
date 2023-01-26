from pytube import YouTube
from datetime import datetime
import sqlite3
import pandas as pd
import re
import string


class ScrapeYouTubeVideoViews:

    url = str
    video_data = YouTube
    _database_name = "YouTubeVideoData.db"
    db_connection = sqlite3.Connection
    db_cursor = sqlite3.Cursor

    def __init__(self, video_url: str, database_name: str = "YouTubeVideoData.db"):
        self.url = video_url
        self.video_data = YouTube(self.url)
        self.database_name = database_name

    def convert_title_to_machine_readable(self) -> str:
        subStr = "[%s ]" % string.punctuation
        return "_" + re.sub(subStr, "_", self.get_video_title())

    def get_video_views(self) -> int:
        return self.video_data.views

    def get_video_title(self) -> str:
        return self.video_data.title

    def get_capture_date_str(self, capture_datetime: datetime = datetime.now()) -> str:
        capture_date_str = capture_datetime.strftime("%Y-%m-%d")
        return capture_date_str

    def table_exists_in_db(self, table_name: str) -> bool:
        return table_name in self.get_all_table_names_in_db()

    def get_all_table_names_in_db(self) -> list:
        list_of_all_table_info = self.db_cursor.execute(
            "SELECT * FROM sqlite_master where type='table'"
        ).fetchall()[:]
        table_names = [table_info[1] for table_info in list_of_all_table_info]
        return table_names

    def add_table_to_db(self, table_name: str):
        self.db_cursor.execute(
            "CREATE TABLE " + table_name + " (capture_date text, views integer)"
        )
        self.db_connection.commit()

    def get_connection_cursor(self) -> sqlite3.Cursor:
        return self.db_connection.cursor()

    def connect_to_database(self) -> sqlite3.Connection:
        return sqlite3.connect(self.database_name)

    def add_scrape_data_to_db_table(self, table_name: str):
        self.db_cursor.execute(
            "INSERT INTO " + table_name + " VALUES (?, ?)",
            (
                self.get_capture_date_str(),
                self.get_video_views(),
            ),
        )
        self.db_connection.commit()

    def get_scrape_data_from_db_table(self, table_name: str) -> pd.DataFrame:
        table_data = self.db_cursor.execute("SELECT * FROM " + table_name).fetchall()
        if table_data == []:
            return pd.DataFrame()
        else:
            column_names_full = self.db_cursor.description
            column_names = [c_name[0] for c_name in column_names_full]
            df = pd.DataFrame(data=table_data, columns=column_names)
            df["capture_date"] = pd.to_datetime(df["capture_date"], format="%Y-%m-%d")
            df = df.set_index("capture_date")
            return df

    @property
    def databse_name(self):
        return self._database_name

    @databse_name.setter
    def database_name(self, new_name: str) -> str:
        self._database_name = new_name
        self.db_connection = self.connect_to_database()
        self.db_cursor = self.get_connection_cursor()

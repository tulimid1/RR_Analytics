import unittest
import datetime
from ScrapeYouTubeVideoViews import ScrapeYouTubeVideoViews
from pytube import YouTube
import sqlite3
import os
import pandas as pd
import numpy as np


class ScrapeYTVideoViewsTEST(unittest.TestCase):
    yt = ScrapeYouTubeVideoViews

    def setUp(self):
        self.yt = ScrapeYouTubeVideoViews(
            video_url="https://www.youtube.com/watch?v=NIzDs0IbAxo",
            database_name=":memory:",
        )

    def tearDown(self):
        self.yt.db_connection.close()

    ## SQL database
    def test_scrape_data_views_is_int(self):
        rnd_vid = ScrapeYouTubeVideoViews(
            "https://www.youtube.com/watch?v=pd-0G0MigUA", database_name=":memory:"
        )
        rnd_vid.add_table_to_db(table_name=rnd_vid.convert_title_to_machine_readable())
        rnd_vid.add_scrape_data_to_db_table(
            table_name=rnd_vid.convert_title_to_machine_readable()
        )
        scrape_df = rnd_vid.get_scrape_data_from_db_table(
            table_name=rnd_vid.convert_title_to_machine_readable()
        )
        self.assertIsInstance(scrape_df["views"].values[0], np.int64)

    def test_scrape_data_index_is_datetime(self):
        rnd_vid = ScrapeYouTubeVideoViews(
            "https://www.youtube.com/watch?v=pd-0G0MigUA", database_name=":memory:"
        )
        rnd_vid.add_table_to_db(table_name=rnd_vid.convert_title_to_machine_readable())
        rnd_vid.add_scrape_data_to_db_table(
            table_name=rnd_vid.convert_title_to_machine_readable()
        )
        scrape_df = rnd_vid.get_scrape_data_from_db_table(
            table_name=rnd_vid.convert_title_to_machine_readable()
        )
        self.assertIsInstance(scrape_df.index, pd.DatetimeIndex)

    def test_add_scrape_data_to_db_df_correct_columns(self):
        rnd_vid = ScrapeYouTubeVideoViews(
            "https://www.youtube.com/watch?v=pd-0G0MigUA", database_name=":memory:"
        )
        rnd_vid.add_table_to_db(table_name=rnd_vid.convert_title_to_machine_readable())
        rnd_vid.add_scrape_data_to_db_table(
            table_name=rnd_vid.convert_title_to_machine_readable()
        )
        scrape_df = rnd_vid.get_scrape_data_from_db_table(
            table_name=rnd_vid.convert_title_to_machine_readable()
        )
        self.assertEqual(scrape_df.index.name, "capture_date")
        self.assertEqual(scrape_df.columns[0], "views")

    def test_get_scrape_data_no_data_return_empty_df(self):
        rnd_vid = ScrapeYouTubeVideoViews(
            "https://www.youtube.com/watch?v=pd-0G0MigUA", database_name=":memory:"
        )
        table_name = "test1"
        rnd_vid.add_table_to_db(table_name=table_name)
        self.assertTrue(rnd_vid.get_scrape_data_from_db_table("test1").empty)

    def test_get_scrape_data_return_pdDF(self):
        rnd_vid = ScrapeYouTubeVideoViews(
            "https://www.youtube.com/watch?v=pd-0G0MigUA", database_name=":memory:"
        )
        table_name = "test1"
        rnd_vid.add_table_to_db(table_name=table_name)
        self.assertIsInstance(
            rnd_vid.get_scrape_data_from_db_table("test1"), pd.DataFrame
        )

    def test_get_scrape_data_from_db(self):
        self.assertTrue("get_scrape_data_from_db_table" in dir(self.yt))

    def test_add_scrape_data_to_db_method(self):
        self.assertTrue("add_scrape_data_to_db_table" in dir(self.yt))

    def test_table_exists_False1(self):
        table_name = "test1"
        self.yt.add_table_to_db(table_name=table_name)
        self.assertFalse(self.yt.table_exists_in_db(table_name="Something_else"))

    def test_table_exist_True1(self):
        table_name = "test1"
        self.yt.add_table_to_db(table_name=table_name)
        self.assertTrue(self.yt.table_exists_in_db(table_name="test1"))

    def test_table_exist_return_bool(self):
        self.assertIsInstance(self.yt.table_exists_in_db("test1"), bool)

    def test_table_exists_in_db_method(self):
        self.assertTrue("table_exists_in_db" in dir(self.yt))

    def test_add_two_tables_to_db(self):
        table_name1 = "test1"
        self.yt.add_table_to_db(table_name=table_name1)
        table_name2 = "test2"
        self.yt.add_table_to_db(table_name=table_name2)
        all_table_names = self.yt.get_all_table_names_in_db()
        self.assertTrue(
            (table_name1 in all_table_names) and (table_name2 in all_table_names)
        )

    def test_add_table_to_db(self):
        table_name = "test1"
        self.yt.add_table_to_db(table_name=table_name)
        all_table_names = self.yt.get_all_table_names_in_db()
        self.assertTrue(table_name in all_table_names)

    def test_get_all_table_names_returns_list(self):
        self.assertIsInstance(self.yt.get_all_table_names_in_db(), list)

    def test_get_all_table_names_in_db_method(self):
        self.assertTrue("get_all_table_names_in_db" in dir(self.yt))

    def test_add_table_to_db_method(self):
        self.assertTrue("add_table_to_db" in dir(self.yt))

    def test_cursor_is_CursorClass(self):
        self.assertIsInstance(self.yt.db_cursor, sqlite3.Cursor)

    def test_cursor_is_attribute(self):
        self.assertTrue(hasattr(self.yt, "db_cursor"))

    def test_connection_is_ConnectionClass(self):
        self.assertIsInstance(self.yt.db_connection, sqlite3.Connection)

    def test_connection_is_attribute(self):
        self.assertTrue(hasattr(self.yt, "db_connection"))

    def test_get_connection_cursor_return_cursor(self):
        rnd_vid = ScrapeYouTubeVideoViews(
            "https://www.youtube.com/watch?v=pd-0G0MigUA", database_name=":memory:"
        )
        self.assertIsInstance(rnd_vid.get_connection_cursor(), sqlite3.Cursor)

    def test_get_connection_cursor_method(self):
        self.assertTrue("get_connection_cursor" in dir(self.yt))

    def test_connect_to_database_return_connection(self):
        rnd_vid = ScrapeYouTubeVideoViews(
            "https://www.youtube.com/watch?v=pd-0G0MigUA", database_name=":memory:"
        )
        self.assertIsInstance(rnd_vid.connect_to_database(), sqlite3.Connection)

    def test_connect_to_database_method(self):
        self.assertTrue("connect_to_database" in dir(self.yt))

    def test_db_cursor_changed_with_changed_db_name(self):
        original_cursor = self.yt.db_cursor
        self.yt.database_name = "new.db"
        new_cursor = self.yt.db_cursor
        self.assertNotEqual(original_cursor, new_cursor)
        os.remove("new.db")

    def test_db_connection_changed_with_changed_db_name(self):
        original_connection = self.yt.db_connection
        self.yt.database_name = "new.db"
        new_connection = self.yt.db_connection
        self.assertNotEqual(original_connection, new_connection)
        os.remove("new.db")

    def test_db_default_name_temp_db(self):
        already_has_youtube_video_data_db = os.path.isfile("YouTubeVideoData.db")
        if already_has_youtube_video_data_db:
            os.rename("YouTubeVideoData.db", "YouTubeVideoData_original.db")
        temp_scrapeYT = ScrapeYouTubeVideoViews(
            video_url="https://www.youtube.com/watch?v=NIzDs0IbAxo"
        )
        temp_scrapeYT.db_connection.close()
        self.assertEqual(
            temp_scrapeYT.database_name,
            "YouTubeVideoData.db",
        )
        os.remove("YouTubeVideoData.db")
        if already_has_youtube_video_data_db:
            os.rename("YouTubeVideoData_original.db", "YouTubeVideoData.db")

    def test_has_database_name_attr(self):
        self.assertTrue(hasattr(self.yt, "database_name"))

    ## Get relevant information from YouTube video
    def test_convert_title_to_machine_readable_ex3(self):
        ex3 = ScrapeYouTubeVideoViews(
            "https://www.youtube.com/watch?v=_654sbErhBw", database_name=":memory:"
        )
        self.assertTrue(ex3.convert_title_to_machine_readable(), "_4_Know_Your_Data")

    def test_convert_title_to_machine_readable_ex2(self):
        ex2 = ScrapeYouTubeVideoViews(
            "https://www.youtube.com/watch?v=bbpbERTfluE", database_name=":memory:"
        )
        self.assertTrue(
            ex2.convert_title_to_machine_readable(), "_Analyzing_Data_in_MATLAB"
        )

    def test_convert_title_to_machine_readable_ex1(self):
        self.assertEqual(
            self.yt.convert_title_to_machine_readable(),
            "_2022_2023_ReproRehab_Leadership_Team_and_TA_Introductions",
        )

    def test_convert_title_to_machine_readable_method(self):
        self.assertTrue("convert_title_to_machine_readable" in dir(self.yt))

    def test_get_video_views_returns_int(self):
        self.assertIsInstance(self.yt.get_video_views(), int)

    def test_get_video_views_method(self):
        self.assertTrue("get_video_views" in dir(self.yt))

    def test_get_video_title_current_video(self):
        self.assertEqual(
            self.yt.get_video_title(),
            "2022-2023 ReproRehab Leadership Team and TA Introductions",
        )

    def test_get_video_title_return_str(self):
        self.assertIsInstance(self.yt.get_video_title(), str)

    def test_get_video_title_method(self):
        self.assertTrue("get_video_title" in dir(self.yt))

    ## YouTube object (title, views, [general scrapped information about youtube video])

    def test_video_data_is_YT_instance(self):
        self.assertIsInstance(self.yt.video_data, YouTube)

    def test_has_video_data_attribute(self):
        self.assertTrue(hasattr(self.yt, "video_data"))

    ## Get date when scraped

    def test_get_capture_date_Dec_25_2023(self):
        expected_capture_date = "2023-12-25"
        dec_25_23 = datetime.datetime(2023, 12, 25)
        actual_capture_date = self.yt.get_capture_date_str(dec_25_23)
        self.assertEqual(actual_capture_date, expected_capture_date)

    def test_get_capture_date_June_21_2023(self):
        expected_capture_date = "2023-06-21"
        june_21_23 = datetime.datetime(2023, 6, 21)
        actual_capture_date = self.yt.get_capture_date_str(june_21_23)
        self.assertEqual(actual_capture_date, expected_capture_date)

    def test_get_capture_date_Jan_1_2023(self):
        expected_capture_date = "2023-01-01"
        jan_1_23 = datetime.datetime(2023, 1, 1)
        actual_capture_date = self.yt.get_capture_date_str(jan_1_23)
        self.assertEqual(actual_capture_date, expected_capture_date)

    def test_get_capture_date_inputDateTime(self):
        self.yt.get_capture_date_str(datetime.datetime.now())

    def test_get_capture_date_method_exist(self):
        self.assertTrue("get_capture_date_str" in dir(self.yt))


if __name__ == "__main__":
    unittest.main()

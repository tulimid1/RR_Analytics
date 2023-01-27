from ScrapeYouTubeVideoViews import ScrapeYouTubeVideoViews
from getYouTubeURLsFromTxT import getYouTubeURLsFromTxT


def addChannelVideoInfo2Database():
    RRchannel_urls = getYouTubeURLsFromTxT()

    for video_url in RRchannel_urls:
        RR_video = ScrapeYouTubeVideoViews(video_url)
        table_already_exists_in_db = RR_video.table_exists_in_db(
            table_name=RR_video.convert_title_to_machine_readable()
        )
        if not table_already_exists_in_db:
            RR_video.add_table_to_db(
                table_name=RR_video.convert_title_to_machine_readable()
            )
        RR_video.add_scrape_data_to_db_table(
            table_name=RR_video.convert_title_to_machine_readable()
        )

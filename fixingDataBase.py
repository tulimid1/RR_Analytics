from ScrapeYouTubeVideoViews import ScrapeYouTubeVideoViews
from getYouTubeURLsFromTxT import getYouTubeURLsFromTxT
from datetime import datetime

now = datetime.now()


RRchannel_urls = getYouTubeURLsFromTxT()

for video_url in RRchannel_urls:

    RR_video = ScrapeYouTubeVideoViews(video_url)

    df = RR_video.extractDataFromDataBase()

    a = 1

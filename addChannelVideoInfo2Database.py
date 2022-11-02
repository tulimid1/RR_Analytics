from ScrapeYouTubeVideoViews import ScrapeYouTubeVideoViews
from getYouTubeURLsFromTxT import getYouTubeURLsFromTxT

def addChannelVideoInfo2Database():
    RRchannel_urls = getYouTubeURLsFromTxT()

    for video_url in RRchannel_urls:
        RR_video = ScrapeYouTubeVideoViews(video_url)
        RR_video.addData2DataBase()

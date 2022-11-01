import pytube as pyt
from ScrapeYouTubeVideoViews import ScrapeYouTubeVideoViews

RRchannel_url = "https://www.youtube.com/channel/UC1bzWxHW5rMuoJeXDD-sEsQ/videos"
RRchannel = pyt.Channel(RRchannel_url)

RR_video_urls = RRchannel.video_urls

for video_url in RR_video_urls:
    RR_video = ScrapeYouTubeVideoViews(video_url)
    RR_video.addData2DataBase()

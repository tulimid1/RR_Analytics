import pytube as pyt

RRchannel = pyt.Channel(
    "https://www.youtube.com/channel/UC1bzWxHW5rMuoJeXDD-sEsQ/featured"
)

RR_video_urls = RRchannel.video_urls

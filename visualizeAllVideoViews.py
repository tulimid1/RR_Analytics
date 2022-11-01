from cProfile import label
import pytube as pyt
from ScrapeYouTubeVideoViews import ScrapeYouTubeVideoViews
import matplotlib.pyplot as plt
import savingfigures as sf

RRchannel_url = "https://www.youtube.com/channel/UC1bzWxHW5rMuoJeXDD-sEsQ/videos"
RRchannel = pyt.Channel(RRchannel_url)

RR_video_urls = RRchannel.video_urls

allVideoFig = plt.figure()
allVideoAx = plt.subplot(1, 1, 1)
for video_url in RR_video_urls:
    RR_video = ScrapeYouTubeVideoViews(video_url)
    RR_video_df = RR_video.extractDataFromDataBase()
    singleVideoFig = plt.figure()
    singleVideoAx = plt.subplot(1, 1, 1)
    singleVideoAx.plot(RR_video_df["views"])
    allVideoAx.plot(RR_video_df["views"])
    singleVideoAx.plot(RR_video_df["views"], marker="o")
    allVideoAx.plot(RR_video_df["views"], marker="o", label=RR_video.title)
    plt.xticks(RR_video_df.index)
    plt.xlabel("Date (yyyy-mm-dd)")
    plt.ylabel("Number of Views")
    plt.title(RR_video.title)
    # plt.show()
    sf.auto_save(fig_obj=singleVideoFig, fig_name=RR_video.db_table_name)

plt.xticks(RR_video_df.index)
plt.xlabel("Date (yyyy-mm-dd)")
plt.ylabel("Number of Views")
# plt.legend(loc=0)
plt.title("All video data")
# plt.show()
sf.auto_save(fig_obj=allVideoFig, fig_name="all_videos")

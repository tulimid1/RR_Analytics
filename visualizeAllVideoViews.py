from cProfile import label
import pytube as pyt
from ScrapeYouTubeVideoViews import ScrapeYouTubeVideoViews
import matplotlib.pyplot as plt
import savingfigures as sf
from getYouTubeURLsFromTxT import getYouTubeURLsFromTxT
import numpy as np


def visualizeAllvideoViews():
    RRchannel_urls = getYouTubeURLsFromTxT()

    allVideoFig = plt.figure()
    allVideoAx = plt.subplot(1, 1, 1)
    for video_url in RRchannel_urls:

        RR_video = ScrapeYouTubeVideoViews(video_url)
        RR_video_df = RR_video.get_scrape_data_from_db_table(
            table_name=RR_video.convert_title_to_machine_readable()
        )

        singleVideoFig = plt.figure()
        singleVideoAx = plt.subplot(1, 1, 1)
        singleVideoAx.plot(RR_video_df["views"])
        allVideoAx.plot(RR_video_df["views"])
        singleVideoAx.plot(RR_video_df["views"], marker="o")
        allVideoAx.plot(
            RR_video_df["views"], marker="o", label=RR_video.get_video_title()
        )
        xTickFreq = int(np.round(len(RR_video_df.index) / 4))
        is_first_run = xTickFreq == 0
        if is_first_run:
            xTickFreq = 1
        plt.xticks(RR_video_df.index[::xTickFreq])
        plt.xlabel("Date (yyyy-mm-dd)")
        plt.ylabel("Number of Views")
        plt.title(RR_video.get_video_title())
        # plt.show()
        sf.auto_save(
            fig_obj=singleVideoFig,
            fig_name=RR_video.convert_title_to_machine_readable(),
        )

    plt.xticks(RR_video_df.index[::xTickFreq])
    plt.xlabel("Date (yyyy-mm-dd)")
    plt.ylabel("Number of Views")
    # plt.legend(loc=0)
    plt.title("All video data")
    # plt.show()
    sf.auto_save(fig_obj=allVideoFig, fig_name="all_videos")

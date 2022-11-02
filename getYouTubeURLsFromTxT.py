import re


def getYouTubeURLsFromTxT():

    with open("watchLinks.txt") as file:
        raw_txt = file.readlines()

    youtubeURL_prefix = "https://www.youtube.com"

    full_video_url = []
    for video_url in raw_txt:
        full_video_url.append(youtubeURL_prefix + re.findall('"(.*?)"', video_url)[0])

    return full_video_url

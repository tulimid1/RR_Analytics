import schedule
import time
from addChannelVideoInfo2Database import addChannelVideoInfo2Database
from visualizeAllVideoViews import visualizeAllvideoViews


def scrapeAndVisualize():
    addChannelVideoInfo2Database()

    visualizeAllvideoViews()


schedule.every().day.at("09:00").do(scrapeAndVisualize)

secondsPerDay = 86400
while True:
    schedule.run_pending()
    time.sleep(secondsPerDay)

import schedule
import time
from getNextRunDateTime import getNextRunDateTime
from addChannelVideoInfo2Database import addChannelVideoInfo2Database
from visualizeAllVideoViews import visualizeAllvideoViews


def scrapeAndVisualize():
    addChannelVideoInfo2Database()

    visualizeAllvideoViews()


schedule.every().day.at("08:45").do(scrapeAndVisualize)

secondsPerDay = 864000
waitTime = secondsPerDay / 80  # every 3 hours
while True:
    schedule.run_pending()
    getNextRunDateTime(waitTime)
    time.sleep(waitTime)

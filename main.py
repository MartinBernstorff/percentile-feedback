# Date and time improts
import datetime
from datetime import datetime as dt
import time

import sys

from credentials import TOGGL_TOKEN
from toggl.TogglPy import Toggl

from pprint import pprint
import urllib

import subprocess

# Basic setup

toggl = Toggl()

toggl.setAPIKey(TOGGL_TOKEN)

offset = int(0)

#Generate today-string
index = dt.today() + datetime.timedelta(-100)
index_midnight = index.replace(hour=0, minute=1)
index_formatted = index_midnight.isoformat() + 'Z'
index_str = dt.strftime(index,'%Y-%m-%d')

day_after_index = index + datetime.timedelta(101)
day_after_index_midnight = day_after_index.replace(hour=0, minute=1)
day_after_index_formatted = day_after_index_midnight.isoformat() + 'Z'

####################################################
# Check if entries already exist in Toggl for date #
####################################################
start_date_encoded = urllib.parse.quote(index_formatted)
end_date_encoded = urllib.parse.quote(day_after_index_formatted)

while True:
    entries = toggl.request("https://www.toggl.com/api/v8/time_entries" + "?start_date=" + start_date_encoded + "&end_date=" + end_date_encoded)

    with open('percentile-feedback/periods.txt', 'w') as periods:
        for entry in entries:
            date = entry["start"][0:10]
            hour = int(entry["start"][11:13]) + 2
            minute = int(entry["start"][14:16])
            second = int(entry["start"][17:19])

            if int(entry["duration"]) < 0:
                duration = int(entry["duration"]) + round(time.time())
            else:
                duration = int(entry["duration"])

            start_seconds = hour * 3600 + minute * 60 + second
            end_seconds = start_seconds + duration

            period_string = date + " " + str(start_seconds) + " " + str(end_seconds)
            print(period_string)

            periods.write(period_string + "\n")

    python2_command = "python percentile-feedback/data.py --convert-log percentile-feedback/periods.txt"

    process = subprocess.Popen(python2_command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    if sys.argv[1] is not "1":
        break

    time.sleep(10)

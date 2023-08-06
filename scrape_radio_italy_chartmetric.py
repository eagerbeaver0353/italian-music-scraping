from driver import Driver
from bs4 import BeautifulSoup
import csv, time
from rich import print
import random
import datetime
import time
from chartmetric import ChartMetricApi
import os
import sys

category = "radio"
country = "Italy"

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
WAIT_TIME_LIMIT = int(os.getenv('WAIT_TIME_LIMIT'))

def getCharts(country_id, charts_date, random_id):

    return chartmetricApi.get_airplay_charts_italy(charts_date)

def writeCharts(country_id, charts_date):
    chart_date_obj = datetime.datetime.strptime(charts_date, '%Y-%m-%d')
    chart_month = chart_date_obj.strftime('%Y-%m')
    output_dir = f'{os.path.dirname(os.path.abspath(__file__))}/output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_dir = f'{output_dir}/{chart_month}'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_dir = f'{output_dir}/{category}'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_path = f'{output_dir}/output_{category}_{country_id}_{charts_date}.csv'
    if os.path.exists(output_path):
        return

    charts = getCharts(country_id, charts_date, random.randint(10000, 99999))

    if charts is None:
        return

    rows = charts['data']
    length = charts['length']

    if len(rows) == 0:
        print("Whoops! no data for the chart you are looking for")
        return

    output_file = open(output_path, 'w+', newline='', encoding='utf8')
    writer = csv.writer(output_file)

    writer.writerow(["position", "title", "artists", "isrc"])
    output_file.flush()

    for index, row in enumerate(rows):
        if (row is None):
            continue
        artists = [row['artist_name']]
        while None in artists:
            artists.remove(None)

        pos = row['rank'] or 10000
        evo = 0
        if row['pre_rank'] is not None:
            evo = row['pre_rank'] - row['rank']
        writer.writerow([pos, row['name'], ", ".join(artists), row.get('isrc', "")])
        output_file.flush()
        # print(row)

def scrape_radio(start_date, end_date):
    now = datetime.datetime.now()
    date_string = now.strftime("%Y-%m-%d %H-%M-%S")

    print("======== Starting the App: Radio ==========")

    # Get the command line arguments
    run_mode = "date-range"

    # initialize chart metric api object
    global chartmetricApi
    chartmetricApi = ChartMetricApi()

    if (run_mode == "date-range"):
        # in case of date-range mode
        if (start_date == ""):
            first_day = datetime.date(now.year, now.month, 1)
            start_date = first_day.strftime("%Y-%m-%d")

        try:
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        except Exception as err:
            print("Invalid date string. please try again")
            print(err)

        start_date = datetime.date(start_date.year, start_date.month, start_date.day)

        # Find the next Sunday
        # days_to_sunday = (6 - start_date.weekday() + 7) % 7
        # start_date = start_date + datetime.timedelta(days=days_to_sunday)

        if end_date is None:
            end_date = datetime.date(now.year, now.month, now.day)
        # delta = datetime.timedelta(days=7)
        delta = datetime.timedelta(days=1)

        while start_date <= end_date:
            print("Radio running for", start_date.strftime("%Y-%m-%d"))
            writeCharts(country, start_date.strftime("%Y-%m-%d"))
            start_date += delta

    else:
        # in case of one-time mode

        print("Radio running for", now.strftime("%Y-%m-%d"))
        writeCharts(country, now.strftime("%Y-%m-%d"))



if __name__ == '__main__s':

    now = datetime.datetime.now()
    date_string = now.strftime("%Y-%m-%d %H-%M-%S")

    print("======== Starting the App: Radio ==========")

    # Get the command line arguments
    mode_arg = "" if not len(sys.argv) > 1 else sys.argv[1] 

    run_mode = ""
    if not mode_arg == '--one-time':
        print("Please select running mode. There are 'date-range' and 'one-time' mode.")
        while True:
            res = input("date-range mode? (Y/n): ").lower()
            if (res == "y" or res == ""):
                run_mode = "date-range"
            elif res == "n":
                run_mode = "one-time"
            else:
                print("Invalid input. Please enter 'y' or 'n'.")
                continue    
            break
    else:
        run_mode = "one-time"

    # initialize chart metric api object
    chartmetricApi = ChartMetricApi()

    if (run_mode == "date-range"):
        # in case of date-range mode
        print("Please input start date. Default would be the first Friday of this month.")

        start_date = None
        while True:
        
            start_date = input("start from (i.e 2023-01-01): ")
            if (start_date == ""):
                first_day = datetime.date(now.year, now.month, 1)
                start_date = first_day.strftime("%Y-%m-%d")

            try:
                start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            except Exception as err:
                print("Invalid date string. please try again")
                print(err)
                continue
            break

        start_date = datetime.date(start_date.year, start_date.month, start_date.day)

        # Find the next Sunday
        days_to_sunday = (6 - start_date.weekday() + 7) % 7
        start_date = start_date + datetime.timedelta(days=days_to_sunday)

        end_date = datetime.date(now.year, now.month, now.day)
        delta = datetime.timedelta(days=7)

        while start_date <= end_date:
            print("running for", start_date.strftime("%Y-%m-%d"))
            writeCharts(country, start_date.strftime("%Y-%m-%d"))
            start_date += delta

    else:
        # in case of one-time mode

        print("running for", now.strftime("%Y-%m-%d"))
        writeCharts(country, now.strftime("%Y-%m-%d"))

from driver import Driver
from bs4 import BeautifulSoup
import csv, time
from rich import print
import random
import datetime
import time
from spotify import SpotifyApi
import os
import sys

category = "Radio"
country = "Italy"

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
WAIT_TIME_LIMIT = int(os.getenv('WAIT_TIME_LIMIT'))

def loginProcess(random_id):
    while True:
        try:
            for driver in DriversPool:
                if driver.is_available() and not driver.has_response():
                    driver.do_login()
                    break
            else:
                time.sleep(1)
                print(f'[{random_id}] Waiting for a driver to be available...')
                continue
            break
        except Exception as err:
            print(err)

    wait_time = 0
    while True:
        try:
            if driver.has_response():
                break
            time.sleep(1)
            print(f'[{random_id}] Waiting for a response...')
            wait_time += 1
            if wait_time == WAIT_TIME_LIMIT: 
                driver.release()
                return
        except Exception as err:
            print(err)
            return False
        
    driver.release()
           
    return True

def getCharts(country_id, charts_date, random_id):

    while True:
        try:
            for driver in DriversPool:
                if driver.is_available() and not driver.has_response():
                    driver.get_charts_radio(country_id, charts_date)
                    break
            else:
                time.sleep(1)
                print(f'[{random_id}] Waiting for a driver to be available...')
                continue
            break
        except Exception as err:
            print(err)

    wait_time = 0
    while True:
        try:
            if driver.has_response():
                break
            time.sleep(1)
            print(f'[{random_id}] Waiting for a response...')
            wait_time += 1
            if wait_time == WAIT_TIME_LIMIT: 
                driver.release()
                return
        except Exception as err:
            print(err)
            return None
        
    soup = BeautifulSoup(driver.get_response(), 'html.parser')

    chart_date_input = soup.find('input', {'id': 'datepicker-chart'})
    chart_date = chart_date_input['value']
    
    data_table = soup.find('table')

    rows = []

    if data_table is not None:

        for tr in data_table.find_all('tr'):
            position = tr.find('td', {'class': 'position'}).contents[0]
            title = tr.find('td', {'class': 'title'}).find('span', {'class': 'title'}).find('a').text.replace('\n', '').strip()
            artists_list = tr.find('td', {'class': 'title'}).find('span', {'class': 'artists'}).find_all('a')
            artists = []
            for item in artists_list:
                artists.append(item.contents[0])
            rows.append({
                'position': position,
                'title': title,
                'artists': artists
            })

    driver.release()
        
    return {
        'date': chart_date,
        'rows': rows
    }

def writeCharts(country_id, charts_date):

    charts = getCharts(country_id, charts_date, random.randint(10000, 99999))

    chart_date = charts['date']
    rows = charts['rows']

    if len(rows) == 0:
        print("Whoops! no data for the chart you are looking for")
        return
    
    chart_date_obj = datetime.datetime.strptime(chart_date, '%Y-%m-%d')
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

    output_file = open(f'{output_dir}/output_{category}_{country_id}_{chart_date}.csv', 'w+', newline='', encoding='utf8')
    writer = csv.writer(output_file)

    writer.writerow(["position", "title", "artists", "isrc"])
    output_file.flush()

    # spotify api object
    spotifyApi = SpotifyApi()

    for row in rows:
        if (row is None):
            continue
        row['isrc'] = spotifyApi.getISRCCode(row['title'])
        writer.writerow([row['position'], row['title'], ", ".join(row['artists']), row['isrc']])
        output_file.flush()
        print(row)

if __name__ == '__main__':

    now = datetime.datetime.now()
    date_string = now.strftime("%Y-%m-%d %H-%M-%S")

    print("======== Starting the App ==========")

    # Get the command line arguments
    mode_arg = "" if not len(sys.argv) > 1 else sys.argv[1] 

    run_mode = ""
    if not mode_arg == '--one-time':
        print("Please select running mode. There are 'date-ranger' and 'one-time' mode.")
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

        # Find the next Friday
        days_to_friday = (4 - start_date.weekday()) % 7
        start_date = start_date + datetime.timedelta(days=days_to_friday)

        end_date = datetime.date(now.year, now.month, now.day)
        delta = datetime.timedelta(days=7)

        DriversSize = 1
        DriversPool = [Driver() for _ in range(DriversSize)]

        loginProcess(random.randint(10000, 99999))

        while start_date <= end_date:
            print("running for", start_date.strftime("%Y-%m-%d"))
            writeCharts(country, start_date.strftime("%Y-%m-%d"))
            start_date += delta

    else:
        # in case of one-time mode
        DriversSize = 1
        DriversPool = [Driver() for _ in range(DriversSize)]

        loginProcess(random.randint(10000, 99999))

        writeCharts(country, None)

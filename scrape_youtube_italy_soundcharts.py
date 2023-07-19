from driver import Driver
from bs4 import BeautifulSoup
import csv, time
from rich import print
import concurrent.futures
import random
import traceback
import re
import datetime
import time
import os
import sys

category = "Youtube"
country = "Italy"

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
WAIT_TIME_LIMIT = int(os.getenv('WAIT_TIME_LIMIT'))

def loginProcess(random_id):
    while True:
        try:
            for driver in DriversPool:
                if driver.is_available() and not driver.has_response():
                    driver.do_login_soundcharts()
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
                    driver.get_charts_youtube_soundcharts(country_id, charts_date)
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
    
    # parentDiv = soup.find('div', class_='ieSLQm')
    dataDiv = soup.select_one('.ieSLQm > div:nth-child(1) > div:nth-child(2) > div')

    rows = []

    if dataDiv is not None:

        for data in dataDiv.children:
            print(data)
            # position = tr.find('td', {'class': 'position'}).contents[0]
            # title = tr.find('td', {'class': 'title'}).find('span', {'class': 'title'}).find('a').text.replace('\n', '').strip()
            # artists_list = tr.find('td', {'class': 'title'}).find('span', {'class': 'artists'}).find_all('a')
            # artists = []
            # for item in artists_list:
            #     artists.append(item.contents[0])
            # regex_pattern = r"[^\w\s]" 
            # plays = re.sub(regex_pattern, "", tr.find('td', {'class': 'plays'}).text).replace('\n', '').strip()
            # rows.append({
            #     'position': position,
            #     'title': title,
            #     'artists': artists,
            #     'plays': plays
            # })

    driver.release()
        
    return rows

def writeCharts(country_id, charts_date):

    rows = getCharts(country_id, charts_date, random.randint(10000, 99999))

    if len(rows) == 0:
        print("Whoops! no data for the chart you are looking for")
        return
    
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

    output_file = open(f'{output_dir}/output_{category}_{country_id}_{charts_date}.csv', 'w+', newline='', encoding='utf8')
    writer = csv.writer(output_file)

    writer.writerow(["", "position", "evo", "title", "artists", "label", "release date", "woc"])
    output_file.flush()

    for index, row in enumerate(rows):
        if (row is None):
            continue
        writer.writerow([index+1, row['position'], row['evo'], row['title'], ", ".join(row['artists']), row['label'], row['release_date'], row['woc']])
        output_file.flush()
        print(row)


if __name__ == '__main__':

    now = datetime.datetime.now()
    date_string = now.strftime("%Y-%m-%d %H-%M-%S")

    print("======== Starting the App ==========")

    # Get the command line arguments
    # mode_arg = "" if not len(sys.argv) > 1 else sys.argv[1] 

    DriversSize = 1
    DriversPool = [Driver() for _ in range(DriversSize)]
    # executor = concurrent.futures.ThreadPoolExecutor(max_workers=DriversSize)
    futures = []

    initial_row = {'process': "login", "description": "do login"}

    loginProcess(random.randint(10000, 99999))

    writeCharts(country, now.strftime("%Y-%m-%d"))

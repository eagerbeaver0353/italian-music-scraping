import csv, time
import random
import datetime
import time
from youtube import YoutubeApi
import os

category = "Youtube_New"
country = "Italy"

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
WAIT_TIME_LIMIT = int(os.getenv('WAIT_TIME_LIMIT'))

def getCharts(country_id, charts_date, random_id):

    return youtubeApi.get_charts()

def writeCharts(country_id, charts_date):

    charts = getCharts(country_id, charts_date, random.randint(10000, 99999))

    now = datetime.datetime.now()
    chart_date = now.strftime("%Y-%m-%d")
    playListId = charts['playlist']
    rows = charts['items']

    print(playListId)

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

    writer.writerow(["No", "Pos", "Evo", "title", "video id", "artists", "views"])
    output_file.flush()

    for index, row in enumerate(rows):
        if (row is None):
            continue
        artists = []
        for artist in row['artists']:
            artists.append(artist['name'])
        writer.writerow([index+1, index+1, '', row['title'], row['videoId'], ", ".join(artists), row['views']])
        output_file.flush()
        print(row)

if __name__ == '__main__':

    now = datetime.datetime.now()
    date_string = now.strftime("%Y-%m-%d %H-%M-%S")

    print("======== Starting the App ==========")

    youtubeApi = YoutubeApi()

    writeCharts(country, None)

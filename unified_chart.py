import csv
import datetime
import os
from datetime import datetime
from dateutil.relativedelta import relativedelta
from custom_utils import extract_date

title_index = {
    "spotify": 1,
    "shazam": 1,
    "radio": 1,
    "youtube": 3,
    "tiktok": 2,
}

channels = ['spotify','youtube','tiktok','radio','shazam']

# get combine music tracks result from all channels of Charts
def combineMusicsFromCharts(musicChannels, month, start_date, end_date):
    output_dir = f'{os.path.dirname(os.path.abspath(__file__))}/output/{month}'

    for channelName in channels:
        if channel_weights[channelName] == 0:
            continue
        output_each_channel = f'{output_dir}/{channelName}'
        if os.path.exists(output_each_channel):
            # check {channelName} files & title list
            for filename in os.listdir(output_each_channel):
                if not os.path.splitext(filename)[1] == ".csv":
                    continue
                file_path = f'{output_each_channel}/{filename}'
                if not os.path.exists(file_path):
                    break
                file_date = extract_date(filename)
                
                # checks if the file is between start_date and end_date
                if start_date <= file_date < end_date:
                    pass
                else:
                    continue

                input_file = open(file_path, 'r', encoding='utf-8')
                reader = csv.reader(input_file)
                next(reader)  # Skip header row
                position = 101
                for row in reader:
                    title = row[title_index[channelName]].strip()
                    if position == 1:
                        break
                    if not title in musicChannels:
                        musicChannels[title] = {'channels': [], 'positions': {}}
                    if not channelName in musicChannels[title]['channels']:
                        musicChannels[title]['channels'].append(channelName)
                    if not channelName in musicChannels[title]['positions']:
                        musicChannels[title]['positions'][channelName] = []
                    musicChannels[title]['positions'][channelName].append(position)
                    position -= 1
    return musicChannels

def calculate_monthly_position(musicChannels):
    for title, item in musicChannels.items():
        positions = item['positions']
        total_points = 0
        musicChannels[title]['monthly_positions'] = {}
        for channel, position_list in positions.items():
            total_points = 0
            for index, position in enumerate(position_list):
                total_points += position
            monthly_position = 0
            if channel == "spotify" or channel == "shazam":
                monthly_position = round(total_points / 7, 2)
            else:
                monthly_position = total_points
            musicChannels[title]['monthly_positions'][channel] = monthly_position
            
    return musicChannels

# get position value with algorithm
# if present on only one channel : sh + 70, rd + 50, TT + 40, YT + 20, SP + 10
# if present on all 5, he earns a - 38
# if present on 4, except shazam, - 35
# if present on all digital - 30
# radio only + one/two digitals (shazam excluded) - 25
def getPosition(row, position):

    if 'radio' in row and (len(row) == 2 or len(row) == 3) and not 'shazam' in row:
        position -= 25
    elif 'spotify' in row and 'shazam' in row and 'youtube' in row and 'tiktok' in row:
        position -= 30
    elif len(row) == 4 and not 'shazam' in row:
        position -= 35
    elif 'spotify' in row and 'shazam' in row and 'radio' in row and 'youtube' in row and 'tiktok' in row:
        position -= 38
    elif len(row) == 1:
        if row[0] == 'spotify':
            position += 10
        if row[0] == 'youtube':
            position += 20
        if row[0] == 'tiktok':
            position += 40
        if row[0] == 'radio':
            position += 50
        if row[0] == 'shazam':
            position += 70

    return position


def generate_unified_chart(start_date, end_date, _channel_weights):
    global channel_weights
    channel_weights = _channel_weights

    now = datetime.now()

    # print("Please input month. Default would be this month")
    # analyze_month = ""
    # while True:
    #     analyze_month = input("target month (i.e 2023-01): ")
    #     if (analyze_month == ""):
    #         analyze_month = now.strftime("%Y-%m")

    #     try:
    #         analyze_month = datetime.strptime(analyze_month, '%Y-%m')
    #     except Exception as err:
    #         print("Invalid month string. please try again")
    #         print(err)
    #         continue
    #     break
    
    current_date = start_date
    musics = {}
    while current_date <= end_date:
        combineMusicsFromCharts(musics, current_date.strftime("%Y-%m"), start_date, end_date)
        current_date += relativedelta(months=1)
    calculate_monthly_position(musics)

    music_tracks = []
    for title, item in musics.items():
        channels = item['channels']
        positions = item['positions']
        monthly_positions = item['monthly_positions']
        total_points = 0
        for channel, position in monthly_positions.items():
            total_points += position + channel_weights[channel]
        music_tracks.append({
            'title': title,
            'channels': channels,
            'positions': monthly_positions,
            # 'finalposition': getPosition(channels, total_points)
            'finalposition': total_points
        })

    music_tracks = sorted(music_tracks, key=lambda x: x['finalposition'], reverse=True)

    start_date_fmt = start_date.strftime("%Y-%m-%d")
    end_date_fmt = end_date.strftime("%Y-%m-%d")

    output_dir = f'{os.path.dirname(os.path.abspath(__file__))}/output'
    sorted_tracks_file = open(f'{output_dir}/{start_date_fmt}_{end_date_fmt}_sorted_music_tracks.csv', 'w+', newline='', encoding='utf8')
    top_tracks_file = open(f'{output_dir}/{start_date_fmt}_{end_date_fmt}_top_music_tracks.csv', 'w+', newline='', encoding='utf8')
    LIMIT_TOP_TRACK = 50
    writer_sorted_tracks = csv.writer(sorted_tracks_file)
    writer_top_tracks = csv.writer(top_tracks_file)

    writer_sorted_tracks.writerow(["Title", "Channel positions", "Ranking position"])
    sorted_tracks_file.flush()
    writer_top_tracks.writerow(["Title", "Channel positions", "Ranking position"])
    top_tracks_file.flush()

    for index, music_track in enumerate(music_tracks):
        channel_positions = []
        for channel, position in music_track['positions'].items():
            channel_positions.append(f"{channel}: {position}")
        row = [music_track['title'], ", ".join(channel_positions), music_track['finalposition']]
        writer_sorted_tracks.writerow(row)
        sorted_tracks_file.flush()
        if index <= LIMIT_TOP_TRACK:
            writer_top_tracks.writerow(row)
            top_tracks_file.flush()

    return f'{output_dir}/{start_date_fmt}_{end_date_fmt}_top_music_tracks.csv'
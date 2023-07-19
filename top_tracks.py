import csv
import datetime
import os

channel_weights = {
    'spotify': 70,
    'youtube': 50,
    'tiktok': 30,
    'radio': 25,
    'shazam': 5
}

# get combine music tracks result from all channels of Charts
def combineMusicsFromCharts(month):

    output_dir = f'{os.path.dirname(os.path.abspath(__file__))}/output/{month}'

    spotify_title_index = 1
    shazam_title_index = 1
    radio_title_index = 1
    youtube_title_index = 3
    tiktok_title_index = 2
    max_count = 100
    
    musicChannels = {}

    output_spotify = f'{output_dir}/Spotify'
    if os.path.exists(output_spotify):
        # check spotify files & title list
        for filename in os.listdir(output_spotify):
            if not os.path.splitext(filename)[1] == ".csv":
                continue
            file_path = f'{output_spotify}/{filename}'
            if not os.path.exists(file_path):
                break
            input_file = open(file_path, 'r', encoding='utf-8')
            reader = csv.reader(input_file)
            next(reader)  # Skip header row
            position = 101
            for row in reader:
                title = row[spotify_title_index].strip()
                if position == 1:
                    break
                if not title in musicChannels:
                    musicChannels[title] = {'channels': [], 'positions': {}}
                if not 'spotify' in musicChannels[title]['channels']:
                    musicChannels[title]['channels'].append('spotify')
                if not 'spotify' in musicChannels[title]['positions']:
                    musicChannels[title]['positions']['spotify'] = []
                musicChannels[title]['positions']['spotify'].append(position)
                position -= 1

    output_shazam = f'{output_dir}/Shazam'
    if os.path.exists(output_shazam):
        # check shazam files & title list
        for filename in os.listdir(output_shazam):
            if not os.path.splitext(filename)[1] == ".csv":
                continue
            file_path = f'{output_shazam}/{filename}'
            if not os.path.exists(file_path):
                break
            input_file = open(file_path, 'r', encoding='utf-8')
            reader = csv.reader(input_file)
            next(reader)  # Skip header row
            position = 101
            for row in reader:
                title = row[shazam_title_index].strip()
                if position == 1:
                    break
                if not title in musicChannels:
                    musicChannels[title] = {'channels': [], 'positions': {}}
                if not 'shazam' in musicChannels[title]['channels']:
                    musicChannels[title]['channels'].append('shazam')
                if not 'shazam' in musicChannels[title]['positions']:
                    musicChannels[title]['positions']['shazam'] = []
                musicChannels[title]['positions']['shazam'].append(position)
                position -= 1

    output_radio = f'{output_dir}/Radio'
    if os.path.exists(output_radio):
        # check radio files & title list
        for filename in os.listdir(output_radio):
            if not os.path.splitext(filename)[1] == ".csv":
                continue
            file_path = f'{output_radio}/{filename}'
            if not os.path.exists(file_path):
                break
            input_file = open(file_path, 'r', encoding='utf-8')
            reader = csv.reader(input_file)
            next(reader)  # Skip header row
            position = 101
            for row in reader:
                title = row[radio_title_index].strip()
                if position == 1:
                    break
                if not title in musicChannels:
                    musicChannels[title] = {'channels': [], 'positions': {}}
                if not 'radio' in musicChannels[title]['channels']:
                    musicChannels[title]['channels'].append('radio')
                if not 'radio' in musicChannels[title]['positions']:
                    musicChannels[title]['positions']['radio'] = []
                musicChannels[title]['positions']['radio'].append(position)
                position -= 1

    output_youtube = f'{output_dir}/Youtube'
    if os.path.exists(output_youtube):
        # check youtube files & title list
        for filename in os.listdir(output_youtube):
            if not os.path.splitext(filename)[1] == ".csv":
                continue
            file_path = f'{output_youtube}/{filename}'
            if not os.path.exists(file_path):
                break
            input_file = open(file_path, 'r', encoding='utf-8')
            reader = csv.reader(input_file)
            next(reader)  # Skip header row
            position = 101
            for row in reader:
                title = row[youtube_title_index].strip()
                if position == 1:
                    break
                if not title in musicChannels:
                    musicChannels[title] = {'channels': [], 'positions': {}}
                if not 'youtube' in musicChannels[title]['channels']:
                    musicChannels[title]['channels'].append('youtube')
                if not 'youtube' in musicChannels[title]['positions']:
                    musicChannels[title]['positions']['youtube'] = []
                musicChannels[title]['positions']['youtube'].append(position)
                position -= 1

    output_tiktok = f'{output_dir}/TikTok'
    if os.path.exists(output_tiktok):
        # check tiktok files & title list
        for filename in os.listdir(output_tiktok):
            if not os.path.splitext(filename)[1] == ".csv":
                continue
            file_path = f'{output_tiktok}/{filename}'
            if not os.path.exists(file_path):
                break
            input_file = open(file_path, 'r', encoding='utf-8')
            reader = csv.reader(input_file)
            next(reader)  # Skip header row
            position = 101
            for row in reader:
                title = row[tiktok_title_index].strip()
                if position == 1:
                    break
                if not title in musicChannels:
                    musicChannels[title] = {'channels': [], 'positions': {}}
                if not 'tiktok' in musicChannels[title]['channels']:
                    musicChannels[title]['channels'].append('tiktok')
                if not 'tiktok' in musicChannels[title]['positions']:
                    musicChannels[title]['positions']['tiktok'] = []
                musicChannels[title]['positions']['tiktok'].append(position)
                position -= 1

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


if __name__ == '__main__':

    now = datetime.datetime.now()

    print("Please input month. Default would be this month")
    analyze_month = ""
    while True:
        analyze_month = input("target month (i.e 2023-01): ")
        if (analyze_month == ""):
            analyze_month = now.strftime("%Y-%m")

        try:
            analyze_month = datetime.datetime.strptime(analyze_month, '%Y-%m')
        except Exception as err:
            print("Invalid month string. please try again")
            print(err)
            continue
        break

    str_month = analyze_month.strftime("%Y-%m")

    musics = combineMusicsFromCharts(str_month)

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

    output_dir = f'{os.path.dirname(os.path.abspath(__file__))}/output/{str_month}'
    sorted_tracks_file = open(f'{output_dir}/{str_month}_sorted_music_tracks.csv', 'w+', newline='', encoding='utf8')
    top_tracks_file = open(f'{output_dir}/{str_month}_top_music_tracks.csv', 'w+', newline='', encoding='utf8')
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

    exit
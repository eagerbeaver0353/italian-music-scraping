import base64
import requests
from sys import exit
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

TOKEN = os.getenv("CHARTMETRIC_API_REFRESH_TOKEN")
HOST = 'https://api.chartmetric.com'

class ChartMetricApi:

    def __init__(self):
        self.authorize()

    def authorize(self):
        auth_url = f'{HOST}/api/token'
        response = requests.post(auth_url, json={"refreshtoken": TOKEN})
        if response.status_code == 200:
            print(response.json())
            self.access_token = response.json().get('token')
            print(self.access_token)
        else:
            print("Authentication failed with error code: ", response.status_code)

        return True
    
    def get(self, uri):
        return requests.get(f'{HOST}{uri}', headers={'Authorization': f'Bearer {self.access_token}'})
    
    def get_youtube_charts_italy(self, chart_date):

        res = self.get('/api/charts/youtube/tracks?date=' + chart_date + '&country_code=it&offset=0&latest=false')
        
        if res.status_code == 200:
            return res.json().get('obj')
        else:
            print("Get Youtube charts with error code: ", res.status_code)
            return None
    
    def get_tiktok_charts_italy(self, chart_date):

        res = self.get('/api/charts/tiktok/tracks?date=' + chart_date + '&offset=0&latest=false&countryChart=true&code2=IT')

        if res.status_code == 200:
            return res.json().get('obj')
        else:
            print("Get TikTok charts with error code: ", res.status_code)
            return None
        
    def get_shazam_charts_italy(self, chart_date):

        res = self.get('/api/charts/shazam?date=' + chart_date + '&offset=0&latest=false&country_code=IT')

        if res.status_code == 200:
            return res.json().get('obj')
        else:
            print("Get Shazam charts with error code: ", res.status_code)
            return None
        
    def get_spotify_charts_italy(self, chart_date):

        res = self.get('/api/charts/spotify?date=' + chart_date + '&offset=0&latest=false&country_code=IT&type=regional&interval=daily')

        if res.status_code == 200:
            return res.json().get('obj')
        else:
            print("Get Spotify charts with error code: ", res.status_code)
            return None
    
    def get_airplay_charts_italy(self, chart_date):

        res = self.get('/api/charts/airplay/tracks?date=' + chart_date + '&since=' + chart_date + '&offset=0&latest=false&country_code=IT&duration=daily')

        if res.status_code == 200:
            return res.json().get('obj')
        else:
            print("Get Airplay charts with error code: ", res.status_code)
            return None
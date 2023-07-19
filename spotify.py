import base64
import requests
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

client_id = os.getenv('SPOTIFY_API_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_API_CLIENT_SECRET')

class SpotifyApi:

    def __init__(self):
        self.authorize()

    def authorize(self):
        auth_url = 'https://accounts.spotify.com/api/token'
        auth_headers = {'Authorization': 'Basic ' + base64.b64encode((client_id + ':' + client_secret).encode('ascii')).decode('ascii')}
        auth_data = {'grant_type': 'client_credentials'}

        response = requests.post(auth_url, headers=auth_headers, data=auth_data)
        if response.status_code == 200:
            print(response.json())
            self.access_token = response.json().get('access_token')
        else:
            print("Authentication failed with error code: ", response.status_code)

        return True
    
    def search(self, q):
        search_url = 'https://api.spotify.com/v1/search'
        search_headers = {'Authorization': f'Bearer {self.access_token}'}
        search_params = {'q': q, 'type': 'track'}
        response = requests.get(search_url, headers=search_headers, params=search_params)
        if response.status_code == 200:
            tracks = response.json().get('tracks')
            # for track in tracks.get('items'):
            #     track_name = track.get('name')
            #     artist_name = track.get('artists')[0].get('name')
            #     print(f'{track_name} by {artist_name}')
            return tracks
        else:
            print("Search request failed with error code: ", response.status_code)

        return None

    def getISRCCode(self, q):

        searchResult = self.search(q)

        if searchResult is not None and len(searchResult['items']) > 0:
            isrcCode = searchResult['items'][0]['external_ids']['isrc']
            return isrcCode

        return None
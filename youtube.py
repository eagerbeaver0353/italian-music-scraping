from dotenv import load_dotenv
import os
from ytmusicapi import YTMusic

load_dotenv()  # Load environment variables from .env file

class YoutubeApi:

    def __init__(self):
        self.authorize()

    def authorize(self):
        # self.ytmusic = YTMusic("oauth.json")
        self.ytmusic = YTMusic()
        return True
    
    def get_charts(self):

        try:

            # playlistId = self.ytmusic.create_playlist("test", "test description")
            # search_results = self.ytmusic.search("Oasis Wonderwall")
            # print(search_results)
            # self.ytmusic.add_playlist_items(playlistId, [search_results[0]['videoId']])

            chartsList = self.ytmusic.get_charts("IT")

            # print(chartsList['videos']['playlist'])
            # items = chartsList['videos']['items']
            # for item in items:
            #     print(item)
            return chartsList['videos']
        
        except Exception as err:
            print(err)

        return None

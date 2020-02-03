import requests
import json


class TwitchGetMethods:

    def __init__(self, username=None, headers=None):
        self.username = username
        self.headers = headers
        self.user_data = self._get_user_data()
        self.user_id = self.get_user_id()

    def __repr__(self):
        return str(self.user_data)

    def _get_user_data(self, printjson=False, save=False):
        response = requests.get(f'https://api.twitch.tv/helix/users?login={self.username}', headers=self.headers)
        resp_data = response.json()
        if save:
            with open(f'{self.username}_data.txt', 'w') as outfile:
                json.dump(resp_data, outfile)
        if printjson:
            print(resp_data)
        return resp_data

    # Gives user ID from JSON file structured from get_user_data
    # Include file extension
    def get_user_id(self):
        return self.user_data['data'][0]['id']

    # given a user_id returns a list of followers
    def get_followers(self, latest_follower = True, total_followers = True):
        response = requests.get(f'https://api.twitch.tv/helix/users/follows?to_id={self.user_id}', headers=self.headers)
        data_resp = response.json()
        output = []
        if latest_follower:
            output.append(data_resp['data'][0]['from_name'])
        if total_followers:
            output.append(data_resp['total'])
        return output

    # gets current title uses same request as get category
    #remove /n
    def get_title(self):
        response = requests.get(f'https://api.twitch.tv/helix/streams?user_id={self.user_id}', headers = self.headers)
        data_resp = response.json()
        return data_resp['data'][0]['title']

    def _get_game_id(self):
        response = requests.get(f'https://api.twitch.tv/helix/streams?user_id={self.user_id}', headers=self.headers)
        data_resp = response.json()
        return data_resp['data'][0]['game_id']

    def get_category(self):
        game_id = self._get_game_id()
        response = requests.get(f'https://api.twitch.tv/helix/games?id={game_id}', headers=self.headers)
        data_resp = response.json()
        return data_resp['data'][0]['name']









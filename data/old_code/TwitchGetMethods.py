import requests
import pickle
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
        data = response.json()
        if save:
            with open(f'{self.username}_data.txt', 'w') as outfile:
                json.dump(data, outfile)
        if printjson:
            print(data)
        return data

    # Gives user ID from JSON file structured from get_user_data
    # Include file extension
    def get_user_id(self, jsonfilename=None):

        if jsonfilename is not None:
            with open(jsonfilename) as json_file:
                data = json.load(json_file)
                data_dict = data['drinking_game'][0]
                user_id = data_dict['id']
                return user_id
        else:
            data_dict = self.user_data['drinking_game'][0]
            user_id = data_dict['id']
            return user_id

    # given a user_id returns a list of followers
    def get_followers(self, save=False):
        response = requests.get(f'https://api.twitch.tv/kraken/channels/{self.user_id}/follows', headers=self.headers)
        data = response.json()
        list_followers = [key['user']['display_name'] for key in data['follows']]
        return list_followers

    # keeps tracks of new followers who have not refollowed
    # main list is the list of all followers before the interation in the pygame loop
    def get_new_followers(self, main_list):
        new_list = self.get_followers()
        old_main_list = main_list
        new = list(set(main_list) ^ set(new_list))
        main_list = list(set(main_list + new))
        return main_list, old_main_list




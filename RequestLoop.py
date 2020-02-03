import TwitchGetMethods
import time
import json


def main_request_loop(requests_queue):

    # Authentication
    data = None
    with open("data/authentication/authentication_data.txt") as json_file:
        data = json.load(json_file)
    headers = {'Accept': 'application/vnd.twitchtv.v5+json',
               'Client-ID': data['CLIENTID'],
               }
    request_method = TwitchGetMethods.TwitchGetMethods(username='vexedkiller0071', headers=headers)
    # variables for loop
    time_request = 30  # Interval of request time
    time_from_last = 0  # Time since last request
    request_dictionary ={'title': None, 'followers': None, 'category': None, 'latest_follower': None}

    while True:
        time_loop = time.time()

        if time_from_last < time_loop:


            request_dictionary['title'] = request_method.get_title().replace('\n','')
            request_dictionary['latest_follower'], request_dictionary['followers'] = request_method.get_followers()
            request_dictionary['category'] = request_method.get_category()
            requests_queue.put(request_dictionary)
            time_from_last = time.time() + time_request


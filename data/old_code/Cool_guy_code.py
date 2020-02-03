import sys, pygame
import time
import json
import irc.bot
import requests
import queue
import threading



speed_queue = queue.Queue()

class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, username, client_id, token, channel):
        self.client_id = client_id
        self.token = token
        self.channel = '#' + channel

        # Get the channel id, we will need this for v5 API calls
        url = 'https://api.twitch.tv/kraken/users?login=' + channel
        headers = {'Client-ID': client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
        r = requests.get(url, headers=headers).json()
        self.channel_id = r['users'][0]['_id']

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        port = 6667
        print('Connecting to ' + server + ' on port ' + str(port) + '...')
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, token)], username, username)

    def on_welcome(self, c, e):
        print('Joining ' + self.channel)

        # You must request specific capabilities before you can use them
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)

    def on_pubmsg(self, c, e):
        # If a chat message starts with an exclamation point, try to run it as a command
        if e.arguments[0][:1] == '!':
            cmd = e.arguments[0].split(' ')[0][1:]
            print('Received command: ' + cmd)
            self.do_command(e, cmd)
        return

    def do_command(self, e, cmd):
        c = self.connection

        # Poll the API to get current game.
        if cmd == "game":
            url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id
            headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
            r = requests.get(url, headers=headers).json()
            c.privmsg(self.channel, r['display_name'] + ' is currently playing ' + r['game'])

        # Poll the API the get the current status of the stream
        elif cmd == "title":
            url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id
            headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
            r = requests.get(url, headers=headers).json()
            c.privmsg(self.channel, r['display_name'] + ' channel title is currently ' + r['status'])

        # Provide basic information to viewers for specific commands
        elif cmd == "raffle":
            message = "This is an example bot, replace this text with your raffle text."
            c.privmsg(self.channel, message)
        elif cmd == "schedule":
            message = "This is an example bot, replace this text with your schedule text."
            c.privmsg(self.channel, message)

        elif cmd == "speed":
            args = e.arguments[0].split(' ')[1:]
            print("speed args:", args)
            if len(args) == 2:
                try:
                    speed_x = int(args[0])
                    speed_y = int(args[1])
                    speed_queue.put([speed_x, speed_y])
                    print("put new speed", speed_x, speed_y)
                except ValueError as e:
                    print(e)
                    return
                except TypeError:
                    print(e)
                    return


        # The command was not recognized
        else:
            c.privmsg(self.channel, "Did not understand command: " + cmd)

def run_irc():
    data = None
    with open('../authentication/authentication_data.txt') as json_file:
        data = json.load(json_file)

    username = 'vexedkiller0071'
    client_id = data['CLIENTID']
    token = data['Token']
    channel = 'vexedkiller0071'

    bot = TwitchBot(username, client_id, token, channel)
    bot.start()


def run_game():
    pygame.init()

    size = width, height = 320, 240
    speed = [2, 2]
    black = 255, 255, 255

    screen = pygame.display.set_mode(size, flags=pygame.DOUBLEBUF)

    ball = pygame.image.load(r'img/shotglass31.png')
    ballrect = ball.get_rect()

    #last_frame = time.time()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        while not speed_queue.empty():
            speed = speed_queue.get_nowait()
            print("game got new speed", speed)

        if type(speed[0]) is not int:
            if type(speed[1]) is not int:
                ballrect = ballrect.move(speed)

                if ballrect.left < 0 or ballrect.right > width:
                    if speed[0] < 1000:
                        speed[0] = -speed[0]
                if ballrect.top < 0 or ballrect.bottom > height:
                    if speed[1] < 1000:
                        speed[1] = -speed[1]

        time.sleep(1 / 60)
        screen.fill(black)
        screen.blit(ball, ballrect)
        pygame.display.flip()
        #current_frame = time.time()
        #print(f"{(current_frame - last_frame) * 1000:3.1f} ms")
        #last_frame = current_frame

irc_thread = threading.Thread(target=run_irc, daemon=True)
irc_thread.start()
run_game()
sys.exit()
import json
import irc.bot
import random
import queue


# e.tags[7]['key'] this looks for mod when it shows up

# Queue objects required for queue_
class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, username, client_id, token, channel, queue_vote, queue_window, super_chat_queue, chat_queue):
        self.client_id = client_id
        self.token = token
        self.channel = '#' + channel
        self.queue_vote = queue_vote
        self.accepting_questions = False
        self.users = set()
        self.list_answers = []
        self.lock = True
        self.queue_window = queue_window
        self.window = self._next_screen()
        self.super_chat_queue = super_chat_queue
        self.chat_queue = chat_queue

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
            self.do_command(e, cmd, accepting_questions=self.accepting_questions)

        return

    def do_command(self, e, cmd, accepting_questions):
        c = self.connection
        ##############COMMANDS FOR EVERYONE ##############
        # Poll the API to get current game.

        # Votes are gathered and organized into a tuple of percents per choice
        if cmd == 'vote':
            # From e object get the message sent
            args = e.arguments[0].split(' ')
            try:
                # If the length of the argument is more than one ignore because it's not a single character
                if (len(args[1])) == 1:
                    # Don't accept questions unless command is given
                    if self.accepting_questions:
                        # If the user has voted before ignore
                        if not e.tags[3]['value'] in self.users:
                            self.users.add(e.tags[3]["value"])
                            self.list_answers.append(args[1])
                            c.privmsg(self.channel, f'{e.tags[3]["value"]} voted for {args[1]}')
                else:
                    c.privmsg(self.channel, f'{e.tags[3]["value"]} has already voted')

            except IndexError:
                c.privmsg(self.channel, f'{e.tags[3]["value"]} did not cast vote')

        if cmd == 'chat':
            message_to_screen_ = e.arguments[0].replace('!chat ', '')
            self.chat_queue.put(message_to_screen_)

        if not self.lock:
            if cmd == 'next':
                a = next(self.window)
                self.queue_window.put(a)


        ##############COMMANDS FOR Mods ##############
        if e.tags[7]['key'] == 'mod':
            # Starts and ends poll
            if cmd == 'SUPER_question':
                if accepting_questions:
                    self.accepting_questions = False
                    test = self._get_number_choice()
                    self.users = set()
                    self.list_answers = []
                    self.queue_vote.put(test)
                else:
                    self.accepting_questions = True
                    c.privmsg(self.channel, f'monkaS monkaS Voting is active monkaS monkaS')

            elif cmd == "SUPER_lock":
                if self.lock:
                    self.lock = False
                else:
                    self.lock = True
                print(f'lock = {self.lock}')

            elif cmd == "SUPER_chat":
                message_to_screen = e.arguments[0].replace('!SUPER_chat ', '')
                self.super_chat_queue.put(message_to_screen)


        # The command was not recognized
        else:
            c.privmsg(self.channel, "Did not understand command: " + cmd)

    # Gets the number of answers for each choice and picks one randomly if there are ties
    def _get_number_choice(self):
        return self.win_answer([(i, self.list_answers.count(i)) for i in set(self.list_answers)])

    # Gets the winning answer for  a list of tuple answers [('a', 10), ('b', 15) ...]
    def win_answer(self, list_tuples):
        max_val = max([i[1] for i in list_tuples])
        list_a = [i for i in list_tuples if i[1] == max_val]
        return random.choice(list_a)

    def _next_screen(self):
        a = 0
        while True:
            a += 1
            if a < 4:
                yield a
            else:
                a = 1
                yield a


def main_twitchbot(command_vote_queue, window_queue, super_chat_queue, chat_queue):
    with open('data/authentication/authentication_data.txt') as json_file:
        data = json.load(json_file)

    username = 'vexedkiller0071'
    client_id = data['CLIENTID']
    token = data['Token']
    channel = 'vexedkiller0071'
    bot = TwitchBot(username, client_id, token, channel, command_vote_queue, window_queue, super_chat_queue, chat_queue)
    bot.start()

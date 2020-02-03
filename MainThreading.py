import TwitchIRCBot
import TwitchPollGame
import RequestLoop
import queue
import threading
import sys

# Used to create a vote command queue
command_vote_queue = queue.Queue()
requests_queue = queue.Queue()
window_queue = queue.Queue()
super_chat_queue = queue.Queue()
chat_queue = queue.Queue()

# Just just threading stuff
irc_thread = threading.Thread(target=TwitchIRCBot.main_twitchbot, daemon=True, args=(command_vote_queue, window_queue, super_chat_queue, chat_queue))
requests_thread = threading.Thread(target=RequestLoop.main_request_loop, daemon=True, args= (requests_queue,))
irc_thread.start()
requests_thread.start()
TwitchPollGame.main_game(command_vote_queue, requests_queue, window_queue, super_chat_queue, chat_queue)
sys.exit()

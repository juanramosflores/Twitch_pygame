import pygame
import PollingContainer
import queue

# command_vote_queue = queue.Queue()

# Dictionaries used for questions
test_dict1 = {'>>> What is the meaning of life': ['Memes', 'Nothing', 'Happiness', '<insert game here>'],
              '>>> What is the worst programming language': ['Python', 'C#', 'Java', 'Assembly']
              }

test_dict2 = {
    ">>> Why did the chicken cross the road": ['To get to the other side', 'It didin\'t', 'To become a dinner',
                                               'For the purpose of this joke'],
    '>>> The square root 69 is': ['8 something', '8.30662386292', '~8', 'IDK']
}
test_dict1.update(test_dict2)


# Blits images to screen based on num_drinks all inputs are required
def blit_screen(surface_obj=None, array_postions=None, pygamedisplay=None, num_drink=0):
    for num, i in enumerate(array_postions):
        if num <= num_drink - 1:
            pygamedisplay.blit(surface_obj, (i))


# creates a list of font objects
def blit_answers(font_obj=None, answers=None, command_list=None):
    return [font_obj.render(f'{command_list[num]} {i}', False, (255, 255, 255)) for num, i in enumerate(answers)]

# checks to see if anything has changed since last request
def compare_dic_val(temp_dict, new_dict, sound_obj=None):
    try:
        if temp_dict is not None:
            if new_dict is not None:
                what_changed = set(key for key in temp_dict if temp_dict[key] != new_dict[key])
                if 'followers' in what_changed:
                    sound_obj.play(0)
    except TypeError:
        pass


# Main game loop, requires a queue object to work
def main_game(command_vote_queue, requests_queue, window_queue, super_chat_queue, chat_queue):
    ########instantiated classes outside of main game loop########
    global latest_follower_render
    pygame.init()
    pygame.font.init()
    questions = PollingContainer.Questions(test_dict1)

    # Dealing With Font
    game_font = pygame.font.Font('data/fonts/font3.otf', 16)
    followers_font = pygame.font.Font('data/fonts/font3.otf', 16)
    subscribers_font = pygame.font.Font('data/fonts/font3.otf', 16)
    title_font = pygame.font.Font('data/fonts/font3.otf', 16)
    latest_follower_font = pygame.font.Font('data/fonts/font3.otf', 16)
    category_font = pygame.font.Font('data/fonts/font3.otf', 16)
    chat_message = pygame.font.Font('data/fonts/font3.otf', 20)  # May require too much data
    chat_screen = pygame.font.Font('data/fonts/font3.otf', 1)
    streamer_screen = pygame.font.Font('data/fonts/font3.otf', 20)

    #stream_chat = streamer_screen.render('GOING TO EAT', False, (255, 0, 0))

    # Create surface of (width, height), and its window.
    main_surface_x, main_surface_y = (512, 288)
    main_surface = pygame.display.set_mode((main_surface_x, main_surface_y))

    ######## Loads all images ########
    shot_glass = pygame.image.load(r'data/img/shotglass31.png').convert_alpha()
    background = pygame.image.load("data/img/space.jpg").convert()
    large_terminal = pygame.image.load("data/img/CMD_new.png").convert()

    ######Load Alert Sounds #########
    rattle_snake = pygame.mixer.Sound('data/sounds/rattlesnakerattle.wav')

    ########Variables in loop#########
    _next_request_time = 0  # dont change
    num_drinks = 0  # Number of drinks consumed, changes the amount of blit shot_images to screen
    temp_requests = None  # User to compare old vs new request data
    window = 1  # used to change windows in terminal loop

    # shot glasses on the screen
    ARRAY_POSITIONS = [[11, 5], [61, 5], [111, 5], [161, 5], [211, 5]]

    # Terminal on screen
    POSLARGEWIN = [0, 0]

    # Position of Text
    followers_pos = [20, 150]
    title_pos = [20, 100]
    latest_follower_pos = [20, 200]
    category_pos = [20, 50]

    # In game switches
    game = False  # used to turn poll image and function on and off
    next_question = True  # used to lock Q
    terminal_bool = False

    while True:

        #### key press behaviors ###
        ev = pygame.event.poll()  # Look for any event
        if ev.type == pygame.QUIT:  # Window close button clicked?
            break  # ... leave game loop

        # increase number of drinks
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_UP:
                num_drinks += 1

        # decrease number of drinks
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_DOWN:
                num_drinks -= 1

        # activates the game section of the loop
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_g:
                if game:
                    game = False
                else:
                    game = True

        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_t:
                if terminal_bool:
                    terminal_bool = False
                else:
                    terminal_bool = True

        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_1:
                window = 1

        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_2:
                window = 2

        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_3:
                window = 3

        # locks q until next question parameter is set
        if next_question == True:
            # Grabs and creates a list to be used for the in game sub loop
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_q:
                    command_list = questions.command_choice
                    question, answers = questions()
                    question_surface = game_font.render(question + '?', False, (255, 255, 255))
                    list_answer_obj = blit_answers(font_obj=game_font, answers=answers, command_list=command_list)
                    percents = None
                    next_question = False

        ##### CHECKS QUEUES #####
        while not command_vote_queue.empty():
            percents = command_vote_queue.get_nowait()
            next_question = True

        while not requests_queue.empty():
            request_dict = requests_queue.get_nowait()
            compare_dic_val(temp_requests, request_dict, sound_obj=rattle_snake)
            temp_requests = request_dict.copy()
            # Font Render
            latest_follower_render = latest_follower_font.render("Latest Follower: " + request_dict['latest_follower'],
                                                                 False, (0, 255, 0))
            followers_render = followers_font.render("Followers: " + str(request_dict['followers']), False,
                                                     (255, 255, 0))
            title_render = title_font.render(request_dict['title'], False, (0, 255, 255))
            category_render = category_font.render(request_dict['category'], False, (0, 255, 255))
            print(f"Channel Request Processed...")

        # window queue
        while not window_queue.empty():
            window = window_queue.get_nowait()

        # chat queue
        while not chat_queue.empty():
            chat_string = chat_queue.get_nowait()
            render_chat_message = chat_screen.render(chat_string, False, (255, 0, 0))
            print(chat_string)


        #super_chat_queue
        while not super_chat_queue.empty():
            super_chat_queue_string = super_chat_queue.get_nowait()
            render_super_chat = streamer_screen.render(super_chat_queue_string, False, (255, 0, 0))
            print(super_chat_queue_string)
        #########question game loop section#########
        if game:
            main_surface.blit(large_terminal, POSLARGEWIN)
            try:
                # blits only the question
                main_surface.blit(question_surface, [8, 30])

                # blits a list of objects to the screen
                for num, i in enumerate(list_answer_obj):
                    if percents is None:
                        main_surface.blit(i, [8, 45 + num * 20])
                    # Too lazy to fix
                    elif percents[0] == 'a' and num == 0:
                        main_surface.blit(i, [8, 58 + num * 20])
                    elif percents[0] == 'b' and num == 1:
                        main_surface.blit(i, [8, 58 + num * 20])
                    elif percents[0] == 'c' and num == 2:
                        main_surface.blit(i, [8, 58 + num * 20])
                    elif percents[0] == 'd' and num == 3:
                        main_surface.blit(i, [8, 58 + num * 20])

            except UnboundLocalError:
                print('Press Q')

        ############Terminal info Loop ###############
        elif terminal_bool:
            # Streamer Data
            if window == 1:
                main_surface.blit(large_terminal, POSLARGEWIN)
                main_surface.blit(followers_render, followers_pos)
                main_surface.blit(title_render, title_pos)
                main_surface.blit(category_render, category_pos)
                main_surface.blit(latest_follower_render, latest_follower_pos)

            # Streamer Message
            if window == 2:
                try:
                    main_surface.blit(large_terminal, POSLARGEWIN)
                    main_surface.blit(render_chat_message, [20, 125])
                except UnboundLocalError:
                    pass

            if window == 3:
                try:
                    main_surface.blit(large_terminal, POSLARGEWIN)
                    main_surface.blit(render_super_chat, [20, 125])
                except UnboundLocalError:
                    pass



        ###############Drinking Mode################
        else:

            main_surface.blit(background, [0, 0])

            # Blits shotglasses to screen
            blit_screen(surface_obj=shot_glass, array_postions=ARRAY_POSITIONS, pygamedisplay=main_surface,
                        num_drink=num_drinks)
        pygame.display.flip()

    pygame.quit()  # Once we leave the loop, close the window.

""" Chat says:  A game where you get points based on the most common answer
implement something to look for commands

!hideanswers <user> changes vote answers A) B) C) D) => B) C) D) A)
!answerseed <user> normal is 1 and not normal
!answer <a>



{'What is the meaning of life': [A,B,C,D], ....}

"""
from collections import OrderedDict
import random




class Questions:

    def __init__(self, dictionary):
        self.dictionary = OrderedDict(dictionary)
        self.questions = self._gather_questions()
        self.answers = self._gather_answers()

        # Random version that will be saved
        self.new_questions = self.questions
        self.new_answers = self.answers
        self.dictionary_new = None

        # Choice List choices left for __call__
        self.choice_list = list(range(0,len(self.answers)))

        # future commands
        self.command_choice = ['!vote a ) ', '!vote b ) ', '!vote c ) ', '!vote d ) ']

    def _gather_questions(self):
        questions = [key for key in self.dictionary]
        return questions

    def _gather_answers(self):
        answers = [self.dictionary[key] for key in self.dictionary]
        return answers

    def __len__(self):
        return len(self.questions)

    def __str__(self):
        return str(self.dictionary)

    def __getitem__(self, item):
        return self.questions[item], self.answers[item]

    def __add__(self, other):
        self_dict = self.dictionary
        other_dict = other.dictionary
        return Questions(OrderedDict(list(self_dict.items()) + list(other_dict.items())))

    def play_all(self):
        command_choice = ['!A)', '!B)', '!C)', '!D)']
        if self.dictionary_new is None:
            self.randomize()
            print('')
            for i in Questions(self):
                print(i[0] + '?')
                for num, j in enumerate(i[1]):
                    print(f'{command_choice[num]} {j}')
                print('')

        else:
            for i in Questions(self.dictionary_new):
                print(i)

    def randomize(self, inplace=True):
        random.seed(random.randint(0, 100))
        if inplace:
            c = list(zip(self.questions, self.answers))
            random.shuffle(c)
            self.questions, self.answers = zip(*c)
            self.dictionary = {self.questions[i]: self.answers[i] for i in range(len(self.questions))}
        else:
            c = list(zip(self.new_questions, self.new_answers))
            random.shuffle(c)
            self.new_questions, self.new_answers = zip(*c)
            self.dictionary_new = dict(zip(self.new_questions, self.new_answers))
            print('test')

    def __call__(self):
        if len(self.choice_list) == 0 :
            self.choice_list = list(range(0, len(self.answers)))
            print('All Questions have been answered, resetting questions...')
            print('')

        choice = random.choice(self.choice_list)
        print(self.questions[choice])
        for num, i in enumerate(self.answers[choice]):
            print(f'{self.command_choice[num]} {i}')
        self.choice_list.remove(choice)
        print('')
        return self.questions[choice], self.answers[choice]








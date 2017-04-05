from telebot import types
import duckduckpy
import numpy as np
from QuestionBotController import Controller

# This is an abstract class for menu item
class MenuNodeInterface:
    def __init__(self, init_dict):
        self.id = init_dict['ID']
        self.parent = init_dict['Parent']
        self.text = init_dict['Text']
        self.inline = init_dict['Inline']
        self.probabilistic = init_dict['Probabilistic']
        self.controller = Controller()

    #This is abstract function
    def display(self, tb, message=None, query=None):
        assert False

    #This is abstract function
    def process(self, tb, message = None, query = None):
        assert False

    def current_position(self):
        return self.id


# This is class for nodes from common dialog to find what user wants
class MenuNodeCommon(MenuNodeInterface):
    def __init__(self, init_dict):
        MenuNodeInterface.__init__(self, init_dict)
        self.children = {}
        for key in init_dict['Children'].keys():
            new_node, reprint_mode = init_dict['Children'][key]
            self.children[key] = new_node

    def _inline_markup(self):
        markup = types.InlineKeyboardMarkup()
        for key in sorted(self.children.keys(), reverse=True):
            markup.add(types.InlineKeyboardButton(text=key, callback_data=key))
        return markup

    def _print_markup(self):
        markup = types.ReplyKeyboardMarkup()
        for key in sorted(self.children.keys(), reverse=True):
            markup.add(types.KeyboardButton(key))
        return markup

    def display(self, tb, message=None, query=None):
        if query is not None and message is None:
            message = query.message
        if self.inline:
            markup = self._inline_markup()
        else:
            markup = self._print_markup()
        reply_text = self.text
        if query is not None and self.inline:
            edit_message = query.message
            result = tb.edit_message_text(chat_id=edit_message.chat.id, message_id=edit_message.message_id,
                                          text=reply_text, reply_markup=markup)
            return result
        return tb.send_message(message.chat.id, reply_text, reply_markup=markup)

    def process(self, tb, message=None, query=None):
        if query is not None and message is None:
            return self.__get_item_by_text(query.data)
        else:
            text = message.text
            return self.__get_item_by_text(text)

    def __get_item_by_text(self, text):
        if text in self.children.keys():
            return self.children[text]
        return self.id


# This is class to get question from user and answer it
class MenuNodeQuestion(MenuNodeInterface):
    def __init__(self, init_dict):
        MenuNodeInterface.__init__(self, init_dict)
        self.force_move = init_dict['ForceMove']
        if self.probabilistic:
            self.probabilities = init_dict['Probabilities']

    def display(self, tb, message=None, query=None):
        if query is not None and message is None:
            message = query.message
        tb.send_message(message.chat.id, self.text)

    def process(self, tb, message=None, query=None):
        if query is not None and message is None:
            message = query.message
        text = message.text
        #reply = duckduckpy.query(message.text)
        #result = u'No idea'
        #if reply.answer != u'':
        #    result = reply.answer
        answer = self.controller.get_answer_for_question(text)
        if answer is None:
            answer = "I don't know, but i will figure it out"
            self.controller.add_question(message)
        tb.send_message(message.chat.id, answer)
        next_node = self.force_move
        if self.probabilistic:
            next_node = np.random.choice(self.probabilities.keys(), size=1, p=self.probabilities.values())[0]
        return next_node

    def current_position(self):
        return self.force_move


# This class for next resolving
class MenuNodeQuestionResolve(MenuNodeInterface):
    def __init__(self, init_dict):
        MenuNodeInterface.__init__(self, init_dict)
        self.force_move = init_dict['ForceMove']

    def display(self, tb, message=None, query=None):
        if query is not None and message is None:
            message = query.message
        tb.send_message(message.chat.id, self.text)

    def process(self, tb, message = None, query = None):
        if query is not None and message is None:
            message = query.message
        # We should display answer here
        text = message.text
        return self.force_move

    def current_position(self):
        return self.force_move


# This is the class for asking questions from user
class MenuNodeReply(MenuNodeInterface):
    def __init__(self, init_dict):
        MenuNodeInterface.__init__(self, init_dict)
        self.force_move = init_dict['ForceMove']
        self.pending_questions = {}

    def display(self, tb, message=None, query=None):
        if message is None:
            from_user = query.from_user
        else:
            from_user = message.from_user
        if query is not None and message is None:
            message = query.message
        # We are displaying answer here
        question = self.controller.get_new_question()
        self.pending_questions[from_user.id] = question
        tb.send_message(message.chat.id, question)

    def process(self, tb, message=None, query=None):
        if message is None:
            from_user = query.from_user
        else:
            from_user = message.from_user
        if query is not None and message is None:
            message = query.message
        text = message.text
        self.controller.add_answer(text, self.pending_questions[from_user.id])
        # We are waiting for answer here
        return self.force_move

    def current_position(self):
        return self.force_move


# Deprecated
class MenuNodeReplyResolve(MenuNodeInterface):
    def __init__(self, init_dict):
        MenuNodeInterface.__init__(self, init_dict)
        self.force_move = init_dict['ForceMove']

    def display(self, tb, message=None, query=None):
        if query is not None and message is None:
            message = query.message
        # We should display answer here
        tb.send_message(message.chat.id, self.text)

    def process(self, tb, message = None, query = None):
        if query is not None and message is None:
            message = query.message
        text = message.text
        return self.force_move

    def current_position(self):
        return self.force_move
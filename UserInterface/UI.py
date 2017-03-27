import yaml
from MenuNode import *
import networkx as nx


class UIController:
    def __init__(self, bot, yaml_dataset):
        self.bot = bot
        try:
            yaml_file = open(yaml_dataset, 'r')
        except IOError as er:
            print 'Error in file', yaml_dataset, '\n', er
            raise er
        self.dataset = yaml.load(yaml_file)
        self.position_table = self.__generate_position_table()
        self.user_state_table = {}

    # Restore classes from yaml file
    def __generate_position_table(self):
        result = {}
        for item in self.dataset['Nodes']:
            key = item['ID']
            if item['Class'] == 'MenuNodeCommon':
                result[key] = MenuNodeCommon(item)
            if item['Class'] == 'MenuNodeQuestion':
                result[key] = MenuNodeQuestion(item)
            if item['Class'] == 'MenuNodeQuestionResolve':
                result[key] = MenuNodeQuestionResolve(item)
            if item['Class'] == 'MenuNodeReply':
                result[key] = MenuNodeReply(item)
            if item['Class'] == 'MenuNodeReplyResolve':
                result[key] = MenuNodeReplyResolve
        return result

    #Main processor function
    def process_message(self, message=None, query=None):
        #Just ID extractor
        tmessage = message
        if query is not None and message is None:
            tmessage = query.message
        # Remember user menu position
        id = tmessage.chat.id
        if id not in self.user_state_table.keys():
            self.user_state_table[id] = 0
        # Process current input from user and select new node
        self.user_state_table[id] = self.position_table[self.user_state_table[id]].process(self.bot, message, query)
        # Display this node and wait for new input
        self.position_table[self.user_state_table[id]].display(self.bot, message, query)


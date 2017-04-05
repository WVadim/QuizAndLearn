from PeeWeeController import *
from IndistinctSearch import compare_questions
import datetime


class Controller:
    def __init__(self):
        pass

    def add_user(self, user_data):
        first_name = user_data.first_name
        second_name = user_data.last_name
        id = user_data.id
        try:
            query_result = Person.get(Person.id == id)
            return query_result
        except:
            new_user = Person(firstname=first_name, secondname=second_name, id=id, joindata=datetime.datetime.now())
            new_user.save(force_insert=True)
            return  new_user

    def find_closet_question(self, target_question):
        questions = Question.select()
        question_closeness = []
        for question in questions:
            question_closeness.append((question, compare_questions(target_question, question.text)))
        question_closeness = sorted(question_closeness, key=lambda x: x[1], reverse=True)
        if len(question_closeness) != 0:
            return question_closeness[0]
        return None
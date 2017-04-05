from PeeWeeController import *
from IndistinctSearch import egoistic_comparator
import datetime
import random


class Controller:
    def __init__(self):
        pass

    def get_user(self, user_data):
        id = user_data.id
        try:
            query_result = Person.get(Person.id == id)
            return query_result
        except:
            return None

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
            return new_user

    def find_closest(self, text, dataset, comparator=egoistic_comparator, threshold=0.5):
        closeness = []
        for item in dataset:
            closeness.append((item, comparator(text, item.text)))
        closeness = sorted(closeness, key=lambda x: x[1], reverse=True)
        closeness = [item for item in closeness if item[1] > threshold]
        if len(closeness) != 0:
            return closeness[0]
        return None

    def find_closest_question(self, target_question):
        dataset = Question.select()
        return self.find_closest(target_question, dataset, egoistic_comparator)

    def find_closet_answer(self, target_answer, question_id):
        dataset = Answer.select().where(Answer.question == question_id)
        return self.find_closest(target_answer, dataset, egoistic_comparator)

    def add_question(self, message):
        user = self.get_user(message.from_user)
        assert user is not None
        data = self.find_closest_question(message.text)
        if data is not None:
            closest_question, value = data
            if value >= 0.99:
                return
        question = Question(creator=user.id, text=message.text)
        question.save(force_insert=True)

    def add_answer(self, answer, question):
        question, dist_question = self.find_closest_question(question)
        assert question is not None
        data = self.find_closet_answer(answer, question.id)
        question.totalanswers += 1
        question.save()
        if data is None:
            new_answer = Answer(question=question.id, text=answer)
            new_answer.save(force_insert=True)
            best_answer = new_answer
        else:
            best_answer, dist = data
            best_answer.frequency += 1
            best_answer.save()
        return best_answer

    def get_answer_for_question(self, question):
        question_in_database = self.find_closest_question(question)
        if question_in_database is None:
            return None
        dataset = Answer.select(Answer.question == id)
        answ_list = [item for item in dataset]
        answ_list = sorted(answ_list, key=lambda x: x.frequency, reverse=True)
        return answ_list[0].text

    def get_new_question(self):
        questions = Question.select().where(Question.totalanswers <= 10)
        data = [item for item in questions]
        if len(questions) == 0:
            data = [item for item in Question.select()]
            if len(data) == 0:
                return ''
        index = random.randint(0, len(data) - 1)
        return data[index].text

import peewee
from PeeWeeController import *
from IndistinctSearch.QuestionComparator import egoistic_comparator

class DBInterace:

    # Class should not be instancieated
    def __init__(self):
        assert False

    @staticmethod
    def s_CreateAnswer(question, text=u'', answer_comparator=egoistic_comparator, threshold=0.5):
        matches = DBInterace.GetMatchAnswers(question, text, answer_comparator, threshold)
        desort = [item[0] for item in sorted(matches, key=lambda x: x[1])]
        if len(desort) != 0:
            return desort[0]
        return DBInterace.CreateAnswer(text=text, question=question)

    @staticmethod
    def GetMatchAnswers(question, text, answer_comparator=egoistic_comparator, threshold=0.5):
        all_answers = DBInterace.GetAnswer(question=question)
        match_answers = [(item, answer_comparator(item.text, text)) for item in all_answers
                         if answer_comparator(item.text, text) <= threshold]
        return sorted(match_answers, key=lambda x: x[1])

    @staticmethod
    def s_CreateQuestion(text=u'', difficulty=None, theme=None, creator=0,
                         question_comparator=egoistic_comparator, threshold=0.5):
        #Chech if question with same text exists
        matches = DBInterace.GetMatchQuestions(text, question_comparator, threshold, theme, difficulty)
        desort = [item[0] for item in sorted(matches, key=lambda x: x[1])]
        if len(desort) != 0:
            return desort[0]
        # Return created question
        if difficulty is None:
            difficulty = 1
        if theme is None:
            theme = 1
        return DBInterace.CreateQuestion(text = text, difficulty=difficulty, theme=theme, creator=creator)

    # Get questions that are close enough to source question
    # Metric for distance is question_comparator, exmaple in IndistinctSearch.QuestionComparator.egoistic_comparator
    # Take all questions, that have distance less than threshold
    @staticmethod
    def GetMatchQuestions(source_question_text, question_comparator=egoistic_comparator,
                          threshold=0.5, theme=None, difficulty=None):
        all_questions = DBInterace.GetQuestion(theme=theme, difficulty=difficulty)
        match_questions = [(item, question_comparator(item.text, source_question_text))
                           for item in all_questions
                           if question_comparator(item.text, source_question_text) <= threshold]
        return sorted(match_questions, key=lambda x: x[1])

    # Method is checking if specified user knows all themes with specified difficulty (or without it if it is None)
    @staticmethod
    def CheckPersonKnowsSeq(person, seq, difficulty=None):
        knows = True
        for name, id in seq:
            knows = knows and len(DBInterace.GetKnowledge(difficulty=difficulty, theme=id, person=person)) != 0
        return knows

    # Safe create theme
    @staticmethod
    def s_CreateTheme(label=u'', parent=0):
        item = DBInterace.GetThemeByLabelAndParent(label, parent)
        if item is not None:
            return item
        else:
            return DBInterace.CreateTheme(label=label, parent=parent)

    # Find theme by fixed label and parent into the theme graph
    @staticmethod
    def GetThemeByLabelAndParent(label=u'', parent=0):
        objects = DBInterace.GetTheme(**locals())
        if len(objects) > 1:
            raise ValueError('Theme duplication detected')
        if len(objects) == 0:
            return None
        return objects[0]

    # This method raising IndexError if there is a situation in theme graph
    # When theme have parent that doesn't exists
    @staticmethod
    def TranslateThemeToSeq(id):
        result = []
        current_id = id
        while current_id != 0:
            theme = DBInterace.AtomicGetTheme(current_id)
            if theme is None:
                raise IndexError('Theme graph inconsistency found for theme id ' + str(current_id))
            name = theme.label
            next_id = theme.parent
            result.append((name, current_id))
            current_id = next_id
        return result

    # Find path into theme graph, that leads to target theme
    @staticmethod
    def GetThemeSequences(label=u''):
        objects = DBInterace.GetTheme(**locals())
        return [DBInterace.TranslateThemeToSeq(item.id) for item in objects]

    # Method will raise ValueError if more than 1 difficulty with fixed tag is already exists
    @staticmethod
    def s_CreateDifficulty(difficulty=u''):
        item = DBInterace.GetDifficultyByLabel(difficulty)
        if item is not None:
            return item
        else:
            return DBInterace.CreateDifficulty(difficulty=difficulty)

    # Get difficulty with fixed label
    @staticmethod
    def GetDifficultyByLabel(label):
        objects = DBInterace.GetDifficulty(difficulty=label)
        if len(objects) > 1:
            raise ValueError("Difficulty duplication detected")
        if len(objects) == 0:
            return None
        return objects[0]

    # Create knowledge, that is suitable for user
    @staticmethod
    def AddUserKnowledge(person, difficulty, theme):
        user_knowledge = DBInterace.GetKnowledge(**locals())
        if len(user_knowledge) != 0:
            return True
        # Check difficulty exists
        diff = DBInterace.AtomicGetDifficulty(id=difficulty)
        if diff is None:
            return False
        theme = DBInterace.AtomicGetTheme(id=theme)
        if theme is None:
            return False
        # Here we know that theme, difficulty exist and user dont know it yet
        DBInterace.CreateKnowledge(difficulty=difficulty, theme=theme, person=person)
        return True


    @staticmethod
    def AtomicGet(id_value, class_value):
        try:
            return class_value.get(class_value.id == id_value)
        except:
            return None

    @staticmethod
    def AtomicGetUser(id):
        return DBInterace.AtomicGet(id, Person)

    @staticmethod
    def AtomicGetQuestion(id):
        return DBInterace.AtomicGet(id, Question)

    @staticmethod
    def AtomicGetAnswer(id):
        return DBInterace.AtomicGet(id, Answer)

    @staticmethod
    def AtomicGetTheme(id):
        return DBInterace.AtomicGet(id, Theme)

    @staticmethod
    def AtomicGetDifficulty(id):
        return DBInterace.AtomicGet(id, Difficulty)

    @staticmethod
    def AtomicGetKnowledge(id):
        return DBInterace.AtomicGet(id, Knowledge)

    @staticmethod
    def AtomicGetSource(id):
        return DBInterace.AtomicGet(id, Source)

    @staticmethod
    def CreateObject(parameters_list, class_value):
        try:
            with database.atomic():
                return class_value.create(**parameters_list)
        except peewee.IntegrityError:
            id = parameters_list.get('id')
            if id is None:
                return None
            return DBInterace.AtomicGet(id, class_value)


    @staticmethod
    def GetObject(parameters_list, class_value):
        id = parameters_list.get('id')
        if id is not None:
            return [DBInterace.AtomicGet(id, class_value)]
        else:
            try:
                query_result = class_value.select()
                for key in parameters_list:
                    if parameters_list.get(key) is not None:
                        query_result = query_result.where(getattr(class_value, key) == parameters_list[key])
                return [item for item in query_result]
            except:
                return []

    @staticmethod
    def UpdateObject(parameters_list, class_value):
        try:
            id = parameters_list.get('id')
            if id is None:
                return False
            with database.atomic():
                del parameters_list['id']
                for key in parameters_list.keys():
                    if parameters_list[key] is None:
                        del parameters_list[key]
                query = class_value.update(**parameters_list).where(class_value.id == id)
                query_val = query.execute()
                return query_val > 0
        except:
            return False

    # ----------USER------------------------------------------------------------

    @staticmethod
    def CreateUser(id, firstname=u'', secondname=u''):
        return DBInterace.CreateObject(locals(), Person)

    @staticmethod
    def GetUser(id=None, firstname=None, secondname=None, joindata=None):
        return DBInterace.GetObject(locals(), Person)

    @staticmethod
    def UpdateUser(id, firstname=None, secondname=None):
        return DBInterace.UpdateObject(locals(), Person)

    # ----------QUESTION--------------------------------------------------------

    @staticmethod
    def CreateQuestion(id=None, text=u'', difficulty=1, theme=1, creator=0, total_answers=0):
        return DBInterace.CreateObject(locals(), Question)

    @staticmethod
    def GetQuestion(id=None, text=None, difficulty=None, theme=None, creator=None, total_answers=None):
        return DBInterace.GetObject(locals(), Question)

    @staticmethod
    def UpdateQuestion(id, text=None, difficulty=None, theme=None, creator=None, total_answers=None):
        return DBInterace.UpdateObject(locals(), Question)

    # ----------THEME-----------------------------------------------------------

    @staticmethod
    def CreateTheme(id=None, label=u'', parent=0):
        return DBInterace.CreateObject(locals(), Theme)


    @staticmethod
    def GetTheme(id=None, label=None, parent=None):
        return DBInterace.GetObject(locals(), Theme)


    @staticmethod
    def UpdateTheme(id, label=None, parent=None):
        return DBInterace.UpdateObject(locals(), Theme)

    # ----------DIFFICULTY------------------------------------------------------

    @staticmethod
    def CreateDifficulty(id=None, difficulty=u''):
        return DBInterace.CreateObject(locals(), Difficulty)

    @staticmethod
    def GetDifficulty(id=None, difficulty=None):
        return DBInterace.GetObject(locals(), Difficulty)

    @staticmethod
    def UpdateDifficulty(id=None, difficulty=None):
        return DBInterace.UpdateObject(locals(), Difficulty)

    # ----------KNOWLEDGE-------------------------------------------------------

    @staticmethod
    def CreateKnowledge(id=None, difficulty=1, theme=1, person=0):
        return DBInterace.CreateObject(locals(), Knowledge)

    @staticmethod
    def GetKnowledge(id=None, difficulty=None, theme=None, person=None):
        return DBInterace.GetObject(locals(), Knowledge)

    @staticmethod
    def UpdateKnowledge(id, difficulty=None, theme=None, person=None):
        return DBInterace.UpdateObject(locals(), Knowledge)

    # ----------SOURCE----------------------------------------------------------

    @staticmethod
    def CreateSource(id=None, difficulty=1, theme=1, website=u''):
        return DBInterace.CreateObject(locals(), Source)

    @staticmethod
    def GetSource(id=None, difficulty=None, theme=None, website=None):
        return DBInterace.GetObject(locals(), Source)

    @staticmethod
    def UpdateSource(id, difficulty=None, theme=None, website=None):
        return DBInterace.UpdateObject(locals(), Source)

    # ----------ANSWER----------------------------------------------------------

    @staticmethod
    def CreateAnswer(id=None, frequency=0, question=1, text=u''):
        return DBInterace.CreateObject(locals(), Answer)

    @staticmethod
    def GetAnswer(id=None, frequency=None, question=None, text=None):
        return DBInterace.GetObject(locals(), Answer)

    @staticmethod
    def UpdateAnswer(id, frequency=None, question=None, text=None):
        return DBInterace.UpdateObject(locals(), Answer)
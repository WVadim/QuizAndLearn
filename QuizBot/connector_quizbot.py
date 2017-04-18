from peewee import *
from classes import *
from datetime import date

database = MySQLDatabase('quizDB', **{'password': '', 'user': 'root'})


# Creating tables
# database.create_tables([Person])
# database.create_tables([Difficulty])
# database.create_tables([Theme])
# database.create_tables([Question])
# database.create_tables([Answer])
# database.create_tables([Knowledge])
# database.create_tables([Source])
# storing data
# c = Person(firstname='Javi',joindata=date(2017, 4, 15), secondname='Pena')
# c.save()
# t = Theme(label='Geography')
# t.save()
# t2 = Theme(label='Entertainment')
# t2.save()
# t3 = Theme(label='History')
# t3.save()
# t4 = Theme(label='Art & Literature')
# t4.save()
# t5 = Theme(label='Science & Nature')
# t5.save()
# t6 = Theme(label='Sports & Leisure')
# t6.save()
# dif=Difficulty(difficulty='Easy')
# dif.save()
# dif2=Difficulty(difficulty='Medium')
# dif2.save()
# dif3=Difficulty(difficulty='Hard')
# dif3.save()
# q=Question(creator=c, difficulty=dif, text='What is the capital city of Spain?', theme=t, totalanswers=4)
# q.save()
# one=Answer(frequency=100, question=q, text='Valencia', correct=False)
# two=Answer(frequency=100, question=q, text='Seville', correct=False)
# three=Answer(frequency=100, question=q, text='Madrid', correct=True)
# four=Answer(frequency=100, question=q, text='Barcelona', correct=False)
# one.save()
# two.save()
# three.save()
# four.save()
# q=Question(creator=c, difficulty=dif, text='What is the capital city of Russia?', theme=t, totalanswers=4)
# q.save()
# one=Answer(frequency=100, question=q, text='London', correct=False)
# two=Answer(frequency=100, question=q, text='Moscow', correct=True)
# three=Answer(frequency=100, question=q, text='Stalingrad', correct=False)
# four=Answer(frequency=100, question=q, text='St. Petersburg', correct=False)
# one.save()
# two.save()
# three.save()
# four.save()
# q=Question(creator=c, difficulty=dif, text='What is the capital city of Montenegro?', theme=t, totalanswers=4)
# q.save()
# one=Answer(frequency=100, question=q, text='Sofia', correct=False)
# two=Answer(frequency=100, question=q, text='Belgrade', correct=False)
# three=Answer(frequency=100, question=q, text='Skopje', correct=False)
# four=Answer(frequency=100, question=q, text='Podgorica', correct=True)
# one.save()
# two.save()
# three.save()
# four.save()

def getQuestions(theme, difficulty):
    qs = []
    themes = Theme.select().where(Theme.label == theme)
    for theme in themes:
        themeid = theme.id

    diffs = Difficulty.select().where(Difficulty.difficulty == difficulty)
    for diff in diffs:
        difficultyid = diff.id

    questions = Question.select().where(Question.theme == themeid, Question.difficulty == difficultyid)
    for question in questions:
        qs.append(question.text)

    return qs


def getAnswers(q):
    ans = []
    answers = Answer.select().join(Question).where(Question.text == q)
    for answer in answers:
        ans.append(answer.text)

    return ans


def checkAnswer(a, q):
    correct = False
    answers = Answer.select().where(Answer.text == a).join(Question).where(Question.text == q)
    for answer in answers:
        if answer.correct:
            correct = True
        else:
            correct = False

    return correct


def getDifficulties():
    dif = []
    for difficulty in Difficulty.select():
        dif.append(difficulty.difficulty)

    return dif


def getThemes():
    t = []
    for theme in Theme.select():
        t.append(theme.label)

    return t

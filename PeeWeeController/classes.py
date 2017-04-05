from peewee import *

database = MySQLDatabase('quizDB', **{'password': 'Falkon54', 'user': 'root'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Users(BaseModel):
    id = PrimaryKeyField(db_column='ID')
    telegramid = IntegerField(db_column='TelegramID', unique=True)

    class Meta:
        db_table = 'users'

class Difficulty(BaseModel):
    difficulty = TextField(db_column='Difficulty')
    id = PrimaryKeyField(db_column='ID')

    class Meta:
        db_table = 'difficulty'

class Theme(BaseModel):
    id = PrimaryKeyField(db_column='ID')
    label = TextField(db_column='Label')
    parent = IntegerField(db_column='Parent', null=True)

    class Meta:
        db_table = 'theme'

class Questions(BaseModel):
    difficulty = ForeignKeyField(db_column='Difficulty', rel_model=Difficulty, to_field='id')
    questionid = PrimaryKeyField(db_column='QuestionID')
    questionmaker = ForeignKeyField(db_column='QuestionMaker', rel_model=Users, to_field='id')
    questiontext = TextField(db_column='QuestionText')
    theme = ForeignKeyField(db_column='Theme', rel_model=Theme, to_field='id')

    class Meta:
        db_table = 'questions'

class Answers(BaseModel):
    answertext = TextField(db_column='AnswerText')
    frequency = IntegerField(db_column='Frequency')
    id = PrimaryKeyField(db_column='ID')
    questionid = ForeignKeyField(db_column='QuestionID', rel_model=Questions, to_field='questionid')

    class Meta:
        db_table = 'answers'

class Knowledge(BaseModel):
    difficulty = ForeignKeyField(db_column='Difficulty', rel_model=Difficulty, to_field='id')
    id = PrimaryKeyField(db_column='ID')
    theme = ForeignKeyField(db_column='Theme', rel_model=Theme, to_field='id')
    userid = ForeignKeyField(db_column='UserID', rel_model=Users, to_field='id')

    class Meta:
        db_table = 'knowledge'

class Resources(BaseModel):
    difficulty = ForeignKeyField(db_column='Difficulty', rel_model=Difficulty, to_field='id')
    id = PrimaryKeyField(db_column='ID')
    resourcesite = TextField(db_column='ResourceSite')
    theme = ForeignKeyField(db_column='Theme', rel_model=Theme, to_field='id')

    class Meta:
        db_table = 'resources'


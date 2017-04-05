from peewee import *

database = MySQLDatabase('quizDB', **{'password': 'Falkon54', 'user': 'root'})


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class Person(BaseModel):
    firstname = TextField(db_column='FirstName', null=True)
    id = PrimaryKeyField(db_column='ID')
    joindata = DateTimeField(db_column='JoinData')
    secondname = TextField(db_column='SecondName', null=True)

    class Meta:
        db_table = 'Person'


class Difficulty(BaseModel):
    difficulty = TextField(db_column='Difficulty')
    id = PrimaryKeyField(db_column='ID')

    class Meta:
        db_table = 'Difficulty'


class Theme(BaseModel):
    id = PrimaryKeyField(db_column='ID')
    label = TextField(db_column='Label')
    parent = IntegerField(db_column='Parent', null=True)

    class Meta:
        db_table = 'Theme'


class Question(BaseModel):
    creator = ForeignKeyField(db_column='Creator', rel_model=Person, to_field='id')
    difficulty = ForeignKeyField(db_column='Difficulty', rel_model=Difficulty, to_field='id')
    id = PrimaryKeyField(db_column='ID')
    text = TextField(db_column='Text')
    theme = ForeignKeyField(db_column='Theme', rel_model=Theme, to_field='id')

    class Meta:
        db_table = 'Question'


class Answer(BaseModel):
    frequency = IntegerField(db_column='Frequency')
    id = PrimaryKeyField(db_column='ID')
    question = ForeignKeyField(db_column='Question', rel_model=Question, to_field='id')
    text = TextField(db_column='Text')

    class Meta:
        db_table = 'Answer'


class Knowledge(BaseModel):
    difficulty = ForeignKeyField(db_column='Difficulty', rel_model=Difficulty, to_field='id')
    id = PrimaryKeyField(db_column='ID')
    person = ForeignKeyField(db_column='Person', rel_model=Person, to_field='id')
    theme = ForeignKeyField(db_column='Theme', rel_model=Theme, to_field='id')

    class Meta:
        db_table = 'Knowledge'


class Source(BaseModel):
    difficulty = ForeignKeyField(db_column='Difficulty', rel_model=Difficulty, to_field='id')
    id = PrimaryKeyField(db_column='ID')
    theme = ForeignKeyField(db_column='Theme', rel_model=Theme, to_field='id')
    website = TextField(db_column='Website', null=True)

    class Meta:
        db_table = 'Source'


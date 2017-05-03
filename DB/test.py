from DBInterface import *

# Create objects
# Check API for creation, almost all parameters unnecessary

print 'Users :'
print DBInterace.CreateUser(1, u'Vasya', u'Pupkin').firstname
print DBInterace.CreateUser(2, u'Vadim', u'Kirilin').firstname

# Use s_CreateTheme instead of CreateTheme, s_ - safe method
# It will allow you to avoid dpulicates in database, such as two themes with tag "Math" and same parents but with different ids
print 'Themes :'
biology_theme = DBInterace.s_CreateTheme(label='Biology', parent=0)
print 'Theme created, label :', biology_theme.label
geography_theme = DBInterace.s_CreateTheme(label='Geography', parent=0)
print 'Theme created, label :', geography_theme.label
biology_mammals = DBInterace.s_CreateTheme(label='Mammals', parent=biology_theme.id)
print 'Theme Biology-Mammals created, label :', biology_mammals.label
geography_mammals = DBInterace.s_CreateTheme(label='Mammals', parent=geography_theme.id)
print 'Theme Geography-Mammals created, label :', geography_mammals.label


# Use s_CreateDifficulty instead of CreateDifficulty, s_ - safe method
# It will allow you to avoid dpulicates in database, such as two difficulties with tag "Hard" but with different ids
print 'Difficulties :'
print DBInterace.s_CreateDifficulty(difficulty='Hard').difficulty
print DBInterace.s_CreateDifficulty(difficulty='Easy').difficulty

knowledge = DBInterace.GetKnowledge(person=1)
print 'Person knowledge :', knowledge

#Let's add to user knowledge of Biology at level 'Hard'

#Knowledge is empty, let's create it
# Notice, that knowledge with id == 1 is a special type of knownedge, called 'UNKNOWN'
# First - get difficulty for fixed name

difficulty = DBInterace.GetDifficultyByLabel('Hard')
if difficulty is None:
    difficulty = DBInterace.s_CreateDifficulty(difficulty='Hard')
hard_id = difficulty.id
print 'Id of difficulty "Hard" is', hard_id

#Now select theme, that user knows
#Firstly get all themes with appropriate label
themes = DBInterace.GetThemeSequences('Biology')
for sequence in themes:
    print 'New sequence :'
    for name, id in sequence:
        print 'Name :', name, 'ID :', id

# Here we have only one Biology label, let's use it
if len(themes) != 1:
    print 'More than one Biology in the database, should be selected on of them'
    exit(0)
biology_sequence = themes[0]
biology_theme_id = biology_sequence[0][1]
print 'Target Biology theme ID :', biology_theme_id
#If there i

is_created_or_exist = DBInterace.AddUserKnowledge(2, hard_id, biology_theme_id)
print 'Knowledge is created or already exists :', is_created_or_exist

# Now let's add Biology-Mammals theme to user knowledge
# First' let us get all sequences for "Mammals"
themes = DBInterace.GetThemeSequences('Mammals')
for sequence in themes:
    print 'New sequence :'
    for name, id in sequence:
        print 'Name :', name, 'ID :', id

target_seq = []
#After, for each sequences, we get if user knows everything except last item
for sequence in themes:
    reduced_seq = sequence[1:]
    marker = DBInterace.CheckPersonKnowsSeq(2, reduced_seq)
    print 'User', 'know' if marker else "don't know", 'about', reduced_seq
    # We assuming, that user dont know about Biology and Geography at the same time
    # If he do, them dedision should be made out of context, for example if user pressed "Biology'
    # And want to have estimation for 'Mammals', it should lead us to select sequence
    # For test pruposes, we can assume that all labels in the graph are unique
    if marker:
        target_seq.append(sequence)

if len(target_seq) != 1:
    print 'More than one Mammals in the database, should be selected on of them'
    exit(0)
mammals_sequence = target_seq[0]
mammals_theme_id = mammals_sequence[0][1]
print 'Target Mammals theme ID :', mammals_theme_id

is_created_or_exist = DBInterace.AddUserKnowledge(2, hard_id, mammals_theme_id)
print 'Knowledge is created or already exists :', is_created_or_exist

# Now let's assume, that Vasya is asking question about biology-mammals
question_text = u'Is cow a mammal?'
#Firstly let us check if such question exists
matches = [item[0] for item in DBInterace.GetMatchQuestions(question_text)]
for item in matches:
    print 'Matching question is', item.text

# Obviously there is no appropriate questions for that topic
# So we need to add this question into the database
question = DBInterace.s_CreateQuestion(text=question_text, creator=1)

# Let's assume, that Vadim is asking for a same question
question_text = u'Is cow a mammal?'
#Firstly let us check if such question exists
matches = [item[0] for item in DBInterace.GetMatchQuestions(question_text)]
for item in matches:
    print 'Matching question is', item.text

# Ok, we have matching question
# Now Vadim may tag it

difficulty = DBInterace.GetDifficultyByLabel('Easy')
if difficulty is None:
    difficulty = DBInterace.s_CreateDifficulty(difficulty='Easy')
easy_id = difficulty.id
print 'Id of difficulty "Easy" is', easy_id

updated = DBInterace.UpdateQuestion(id=question.id, difficulty=easy_id)
print 'Updated :', updated
question = DBInterace.AtomicGetQuestion(question.id)
print 'Question difficulty :', question.difficulty.difficulty

# Now, is Vasya will answer the question

answer_text = 'Yes'
matches = [item[0] for item in DBInterace.GetMatchAnswers(question.id, answer_text)]
for item in matches:
    print 'Matching answer for question', question.text, 'is', item.text

# Obviously we dont have maching answers

answer = DBInterace.s_CreateAnswer(question.id, answer_text)
DBInterace.UpdateAnswer(answer.id, answer.frequency + 1)

# Now frequency is updated for matching answer!
# Try to select again, and you will see

matches = [item[0] for item in DBInterace.GetMatchAnswers(question.id, answer_text)]
for item in matches:
    print 'Matching answer for question', question.text, 'is', item.text


# How long is meter?
text = u'How long is meter?'
list_of_question = DBInterace.GetMatchQuestions(text)

if list_of_question == []:
    #create auestion
    pass
else:
    best_match = list_of_question[0]
    id_of_best_match = best_match.id
    answers = DBInterace.GetAnswer(id=id_of_best_match)
    answers = sorted(answers, key=lambda x : x.frequency, reverse=True)
    best_answer = answers[0]


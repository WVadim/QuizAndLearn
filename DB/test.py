from DBInterface import *

# Create objects
#Check API for creation, almost all parameters unnecessary
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
geography_mammals = DBInterace.s_CreateTheme(label='Arts',  parent=0)
geography_mammals = DBInterace.s_CreateTheme(label='Enterteinment',  parent=0)
geography_mammals = DBInterace.s_CreateTheme(label='History',  parent=0)
geography_mammals = DBInterace.s_CreateTheme(label='Science & Technology',  parent=0)
geography_mammals = DBInterace.s_CreateTheme(label='Sports',  parent=0)

# Use s_CreateDifficulty instead of CreateDifficulty, s_ - safe method
# It will allow you to avoid dpulicates in database, such as two difficulties with tag "Hard" but with different ids
print 'Difficulties :'
print DBInterace.s_CreateDifficulty(difficulty='Easy').difficulty
print DBInterace.s_CreateDifficulty(difficulty='Medium').difficulty
print DBInterace.s_CreateDifficulty(difficulty='Hard').difficulty


question1= DBInterace.s_CreateQuestion(text="What is the location of London's National Gallery?",difficulty=3,theme=5,creator=1)
question2= DBInterace.s_CreateQuestion(text="What nationality was Edvard Munch, who produced the famous painting The Scream in 1893?",difficulty=2,theme=5,creator=1)
question3= DBInterace.s_CreateQuestion(text="Pablo Picasso was born in 1881 in which Spanish city?",difficulty=2,theme=5,creator=1)
question4= DBInterace.s_CreateQuestion(text="Which Dutch artist painted the Laughing Cavalier in 1624?",difficulty=1,theme=5,creator=1)
question5= DBInterace.s_CreateQuestion(text="Which English artist painted Rain, Steam and Speed - The Great Western Railway in 1844?",difficulty=1,theme=5,creator=1)
question6= DBInterace.s_CreateQuestion(text="What is the colloquial name for the 1871 painting Arrangement in Grey and Black: The Artist's Mother?",difficulty=1,theme=5,creator=1)
question7= DBInterace.s_CreateQuestion(text="Between 1887 and 1888 Vincent van Gogh produced a series of still life paintings depicting which flowers?",difficulty=2,theme=5,creator=1)
question8= DBInterace.s_CreateQuestion(text="The English artist George Stubbs, who died in 1806, is best remembered for his paintings of what?",difficulty=2,theme=5,creator=1)
question9= DBInterace.s_CreateQuestion(text="Who created the modern sculpture Angel of the North, that overlooks the A1 road and the East Coast main line in Gateshead?",difficulty=1,theme=5,creator=1)
question10= DBInterace.s_CreateQuestion(text="Hans Holbein the Younger was criticized by Henry VIII for painting a flattering portrait of whom?",difficulty=2,theme=5,creator=1)
question11= DBInterace.s_CreateQuestion(text="What spoiled Becky and Steve's wedding reception in Coronation Street last week?",difficulty=2,theme=6,creator=1)
question12= DBInterace.s_CreateQuestion(text="The BBC announced last week that which former presenter has set up his own version of the Blue Peter garden in Edinburgh?",difficulty=1,theme=6,creator=1)
question13= DBInterace.s_CreateQuestion(text="Who plays the title role in the film The Time Traveler's Wife, released last Friday?",difficulty=3,theme=6,creator=1)
question14= DBInterace.s_CreateQuestion(text="Which celebrity signed a 1.5 million deal last week to publish a cookbook?",difficulty=2,theme=6,creator=1)
question15= DBInterace.s_CreateQuestion(text="What is the title of Beyonce's latest single, that reached No 5 in the charts last week?",difficulty=3,theme=6,creator=1)
question16= DBInterace.s_CreateQuestion(text="The new Quentin Tarantino film Inglourious Basterds, due for release on Friday, is set during which war?",difficulty=2,theme=6,creator=1)
question17= DBInterace.s_CreateQuestion(text="Which rock band last week released a 20th anniversary edition of their debut album?",difficulty=2,theme=6,creator=1)
question18= DBInterace.s_CreateQuestion(text="The BBC announced last week that which Radio 1 DJ is to leave the station due to a scheduling shake-up?",difficulty=2,theme=6,creator=1)
question19= DBInterace.s_CreateQuestion(text="Which EastEnders character last week followed his lady- love Brenda as she emigrated to Madeira?",difficulty=1,theme=6,creator=1)
question20= DBInterace.s_CreateQuestion(text="What is the real name of the Big Brother housemate Halfwit, who was evicted from the show last week?",difficulty=3,theme=6,creator=1)
question21= DBInterace.s_CreateQuestion(text="Which German city lies farthest south - Dortmund, Duisburg, Essen or Leipzig?",difficulty=2,theme=2,creator=1)
question22= DBInterace.s_CreateQuestion(text="Of Greece's 2000 islands, how many are inhabited?",difficulty=3,theme=2,creator=1)
question23= DBInterace.s_CreateQuestion(text="What is the administrative centre of County Kildare in Ireland?",difficulty=1,theme=2,creator=1)
question24= DBInterace.s_CreateQuestion(text="Near which Italian city is Frascati wine produced?",difficulty=1,theme=2,creator=1)
question25= DBInterace.s_CreateQuestion(text="In which country is Lake Balaton?",difficulty=1,theme=2,creator=1)
question26= DBInterace.s_CreateQuestion(text="Which Spanish city contains the Alcazar, whose construction began in 1531?",difficulty=3,theme=2,creator=1)
question27= DBInterace.s_CreateQuestion(text="Famous for its local cheese, near which city is Roquefort located?",difficulty=3,theme=2,creator=1)
question28= DBInterace.s_CreateQuestion(text="Of which sport is \"pesapallo\" a local Finnish variation?",difficulty=3,theme=2,creator=1)
question29= DBInterace.s_CreateQuestion(text="Which European country was ruled until 1985 by Enver Hoxha?",difficulty=2,theme=2,creator=1)
question30= DBInterace.s_CreateQuestion(text="Which has the largest population - Bremen, Lille, Ljubljana or Reykjavik?",difficulty=3,theme=2,creator=1)
question31= DBInterace.s_CreateQuestion(text="Approximately how many men did the British lose at the Battle of Jutland in 1916?",difficulty=1,theme=7,creator=1)
question32= DBInterace.s_CreateQuestion(text="In which year did Chaucer complete \"The Canterbury Tales\"?",difficulty=3,theme=7,creator=1)
question33= DBInterace.s_CreateQuestion(text="Of which independent state did Kwame Nkrumah become the first Prime Minister?",difficulty=2,theme=7,creator=1)
question34= DBInterace.s_CreateQuestion(text="In which year was Marie-Antoinette executed?",difficulty=1,theme=7,creator=1)
question35= DBInterace.s_CreateQuestion(text="Where did the Venetian merchant and adventurer Marco Polo die?",difficulty=2,theme=7,creator=1)
question36= DBInterace.s_CreateQuestion(text="In which year did the Middle East's \"Six Day War\" take place?",difficulty=1,theme=7,creator=1)
question37= DBInterace.s_CreateQuestion(text="Against which country did Russia wage war in 1904-05?",difficulty=3,theme=7,creator=1)
question38= DBInterace.s_CreateQuestion(text="Founded in 1746, which is the fourth-oldest university in the USA?",difficulty=2,theme=7,creator=1)
question39= DBInterace.s_CreateQuestion(text="During the reign of Gustav IV, which country lost the territory of Finland in 1808?",difficulty=2,theme=7,creator=1)
question40= DBInterace.s_CreateQuestion(text="In which country did the South American freedom fighter Simon Bolivar die in 1830?",difficulty=1,theme=7,creator=1)
question41= DBInterace.s_CreateQuestion(text="Who co-founded the Apple Corporation with Steve Wozniak in 1976?",difficulty=3,theme=8,creator=1)
question42= DBInterace.s_CreateQuestion(text="What do the initials stand for in the name of the US television network PBS?",difficulty=1,theme=8,creator=1)
question43= DBInterace.s_CreateQuestion(text="In September 1961 Border Television began transmitting from where?",difficulty=1,theme=8,creator=1)
question44= DBInterace.s_CreateQuestion(text="In 1792 the French inventor Claude Chappe built the world's first practical semaphore system between Paris and which other city?",difficulty=3,theme=8,creator=1)
question45= DBInterace.s_CreateQuestion(text="In which US state are the headquarters of the Microsoft Corporation?",difficulty=2,theme=8,creator=1)
question46= DBInterace.s_CreateQuestion(text="When ITV began broadcasting in 1955, what was the first product to be advertised?",difficulty=1,theme=8,creator=1)
question47= DBInterace.s_CreateQuestion(text="Which comedian made the UK's first mobile phone call on I January 1985?",difficulty=1,theme=8,creator=1)
question48= DBInterace.s_CreateQuestion(text="Which piece of computer hardware was invented by Douglas Engelbart in the USA in 1964?",difficulty=2,theme=8,creator=1)
question49= DBInterace.s_CreateQuestion(text="What stopped BBC from broadcasting on its intended launch date of 20 April 1964?",difficulty=3,theme=8,creator=1)
question50= DBInterace.s_CreateQuestion(text="Which offshore radio station began broadcasting on Easter Sunday 1965?",difficulty=2,theme=8,creator=1)
question51= DBInterace.s_CreateQuestion(text="Former England football manager Bobby Robson, who died last week, was born in which County Durham mining village?",difficulty=3,theme=9,creator=1)
question52= DBInterace.s_CreateQuestion(text="Edgbaston, the venue for this year's third Ashes test, is the home of which cricketing county?",difficulty=2,theme=9,creator=1)
question53= DBInterace.s_CreateQuestion(text="Which US TV network is to broadcast live Premier League games this coming season, following the collapse of Setanta?",difficulty=3,theme=9,creator=1)
question54= DBInterace.s_CreateQuestion(text="Which golf course staged this year's British Women's Open?",difficulty=1,theme=9,creator=1)
question55= DBInterace.s_CreateQuestion(text="Spurs beat Hull City last week in the final of the Asia Cup, in which city?",difficulty=2,theme=9,creator=1)
question56= DBInterace.s_CreateQuestion(text="What is the name of the contract recently signed by the FIA and the Formula One Teams' Association?",difficulty=2,theme=9,creator=1)
question57= DBInterace.s_CreateQuestion(text="Which 2009 Tour de France stage winner was suspended last week after testing positive for the blood-booster EPO?",difficulty=3,theme=9,creator=1)
question58= DBInterace.s_CreateQuestion(text="The 2013 Rugby League World Cup, recently awarded to Britain, will be contested by how many teams?",difficulty=1,theme=9,creator=1)
question59= DBInterace.s_CreateQuestion(text="Serena Williams was knocked out of the Bank of the West tennis tournament in Stanford, California last week by Samantha Stosur",difficulty=3,theme=9,creator=1)
question60= DBInterace.s_CreateQuestion(text="The Goodwood Cup was won last Thursday by Schiaparelli. Who was the winning jockey?",difficulty=3,theme=9,creator=1)


answer1 =DBInterace.s_CreateAnswer(1,"Trafalgar Square")
answer2 =DBInterace.s_CreateAnswer(2,"Norwegian")
answer3 =DBInterace.s_CreateAnswer(3,"Malaga")
answer4 =DBInterace.s_CreateAnswer(4,"Frans Hals")
answer5 =DBInterace.s_CreateAnswer(5,"J M W Turner")
answer6 =DBInterace.s_CreateAnswer(6,"Whistler's Mother")
answer7 =DBInterace.s_CreateAnswer(7,"Sunflowers")
answer8 =DBInterace.s_CreateAnswer(8,"Horses")
answer9 =DBInterace.s_CreateAnswer(9,"Antony Gormley")
answer10 =DBInterace.s_CreateAnswer(10,"Anne of Cleves")
answer11 =DBInterace.s_CreateAnswer(11,"A drugs raid")
answer12 =DBInterace.s_CreateAnswer(12,"Peter Duncan")
answer13 =DBInterace.s_CreateAnswer(13,"Rachel McAdams")
answer14 =DBInterace.s_CreateAnswer(14,"Peter Andre")
answer15 =DBInterace.s_CreateAnswer(15,"Sweet Dreams")
answer16 =DBInterace.s_CreateAnswer(16,"World War II")
answer17 =DBInterace.s_CreateAnswer(17,"Stone Roses")
answer18 =DBInterace.s_CreateAnswer(18,"Steve Lamacq")
answer19 =DBInterace.s_CreateAnswer(19,"Charlie Slater")
answer20 =DBInterace.s_CreateAnswer(20,"Freddie Fisher")
answer21 =DBInterace.s_CreateAnswer(21,"Leipzig")
answer22 =DBInterace.s_CreateAnswer(22,"170")
answer23 =DBInterace.s_CreateAnswer(23,"Naas")
answer24 =DBInterace.s_CreateAnswer(24,"Rome")
answer25 =DBInterace.s_CreateAnswer(25,"Hungary")
answer26 =DBInterace.s_CreateAnswer(26,"Toledo")
answer27 =DBInterace.s_CreateAnswer(27,"Toulouse")
answer28 =DBInterace.s_CreateAnswer(28,"Baseball")
answer29 =DBInterace.s_CreateAnswer(29,"Albania")
answer30 =DBInterace.s_CreateAnswer(30,"Bremen")
answer31 =DBInterace.s_CreateAnswer(31,"6300")
answer32 =DBInterace.s_CreateAnswer(32,"Unfinished at the time of his death")
answer33 =DBInterace.s_CreateAnswer(33,"Ghana")
answer34 =DBInterace.s_CreateAnswer(34,"1793")
answer35 =DBInterace.s_CreateAnswer(35,"Venice")
answer36 =DBInterace.s_CreateAnswer(36,"1967")
answer37 =DBInterace.s_CreateAnswer(37,"Japan")
answer38 =DBInterace.s_CreateAnswer(38,"Princeton")
answer39 =DBInterace.s_CreateAnswer(39,"Sweden")
answer40 =DBInterace.s_CreateAnswer(40,"Colombia")
answer41 =DBInterace.s_CreateAnswer(41,"Steve Jobs")
answer42 =DBInterace.s_CreateAnswer(42,"Public Broadcasting Service")
answer43 =DBInterace.s_CreateAnswer(43,"Carlisle")
answer44 =DBInterace.s_CreateAnswer(44,"Lille")
answer45 =DBInterace.s_CreateAnswer(45,"Washington")
answer46 =DBInterace.s_CreateAnswer(46,"Toothpaste")
answer47 =DBInterace.s_CreateAnswer(47,"Venice")
answer48 =DBInterace.s_CreateAnswer(48,"The mouse")
answer49 =DBInterace.s_CreateAnswer(49,"A power cut")
answer50 =DBInterace.s_CreateAnswer(50,"Radio Caroline")
answer51 =DBInterace.s_CreateAnswer(51,"Sacriston ")
answer52 =DBInterace.s_CreateAnswer(52,"Warwickshire")
answer53 =DBInterace.s_CreateAnswer(53,"ESPN")
answer54 =DBInterace.s_CreateAnswer(54,"Royal Lytham")
answer55 =DBInterace.s_CreateAnswer(55,"Beijing")
answer56 =DBInterace.s_CreateAnswer(56,"Concorde Agreement")
answer57 =DBInterace.s_CreateAnswer(57,"Mikel Astarloza")
answer58 =DBInterace.s_CreateAnswer(58,"12")
answer59 =DBInterace.s_CreateAnswer(59,"What nationality is Stosur?")
answer60 =DBInterace.s_CreateAnswer(60,"Frankie Dettori")


DBInterace.CreateSource(id=None,difficulty=1,theme=1,website=u'https://es.coursera.org/learn/dog-emotion-and-cognition')
DBInterace.CreateSource(id=None,difficulty=2,theme=1,website=u'https://es.coursera.org/learn/dog-emotion-and-cognition')
DBInterace.CreateSource(id=None,difficulty=3,theme=1,website=u'https://es.coursera.org/learn/dog-emotion-and-cognition')
DBInterace.CreateSource(id=None,difficulty=1,theme=2,website=u'https://alison.com/course/Google-Earth')
DBInterace.CreateSource(id=None,difficulty=2,theme=2,website=u'https://alison.com/course/Google-Earth')
DBInterace.CreateSource(id=None,difficulty=3,theme=2,website=u'https://alison.com/course/Google-Earth')
DBInterace.CreateSource(id=None,difficulty=1,theme=3,website=u'https://es.coursera.org/learn/animal-behaviour')
DBInterace.CreateSource(id=None,difficulty=2,theme=3,website=u'https://es.coursera.org/learn/animal-behaviour')
DBInterace.CreateSource(id=None,difficulty=3,theme=3,website=u'https://es.coursera.org/learn/animal-behaviour')
DBInterace.CreateSource(id=None,difficulty=1,theme=5,website=u'https://es.coursera.org/learn/art-activity')
DBInterace.CreateSource(id=None,difficulty=2,theme=5,website=u'https://es.coursera.org/learn/art-activity')
DBInterace.CreateSource(id=None,difficulty=3,theme=5,website=u'https://es.coursera.org/learn/art-activity')



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



DBInterace.UpdateAnswer(answer1.id, answer1.frequency + 1)
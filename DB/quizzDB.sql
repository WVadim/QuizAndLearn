DROP DATABASE IF EXISTS quizDB;

SELECT 'DATABASE DROPPED' AS '';

CREATE DATABASE quizDB;

USE quizDB;

CREATE TABLE Person (
	ID				INT UNSIGNED	NOT NULL,
	PRIMARY KEY (ID),
	FirstName			TEXT		,
	SecondName			TEXT		,
	JoinData			DATETIME	NOT NULL DEFAULT CURRENT_TIMESTAMP
);

SELECT 'PERSON TABLE CREATED' AS '';

INSERT INTO Person (ID, FirstName, SecondName) VALUE (0, 'UNKNOWN', 'UNKNOWN');

SELECT * FROM Person;

CREATE TABLE Difficulty (
	ID				INT UNSIGNED	NOT NULL AUTO_INCREMENT,
	PRIMARY KEY (ID),
	Difficulty			TINYTEXT	NOT NULL
);

SELECT 'DIFFICULTY TABLE CREATED' AS '';

INSERT INTO Difficulty (Difficulty) VALUE ('UNKNOWN');

SELECT * FROM Difficulty;

CREATE TABLE Theme (
	ID				INT UNSIGNED	NOT NULL AUTO_INCREMENT,	#Table of the different themes. Each theme can have a parent.
	PRIMARY KEY (ID),
	Label				TINYTEXT	NOT NULL,			#So we have a tree
	Parent				INT UNSIGNED	DEFAULT 1
);

SELECT 'THEME TABLE CREATED' AS '';

INSERT INTO Theme (Label, Parent) VALUE ('UNKNOWN', 0);

SELECT * FROM Theme;

CREATE TABLE Knowledge (
	ID				INT UNSIGNED	NOT NULL AUTO_INCREMENT,	#Storage of the knowledge of each user in a specific theme
	PRIMARY KEY(ID),
	Person				INT UNSIGNED	NOT NULL DEFAULT 0,
	Difficulty			INT UNSIGNED	NOT NULL DEFAULT 0,
	Theme				INT UNSIGNED	NOT NULL DEFAULT 0
);

ALTER TABLE Knowledge	ADD CONSTRAINT KnowledgeUser 	FOREIGN KEY (Person)	 	REFERENCES Person(ID);
ALTER TABLE Knowledge	ADD CONSTRAINT KnowledgeDiff	FOREIGN KEY (Difficulty)	REFERENCES Difficulty(ID);
ALTER TABLE Knowledge	ADD CONSTRAINT KnowledgeTheme 	FOREIGN KEY (Theme)	 	REFERENCES Theme(ID);

SELECT 'KNOWLEDGE TABLE CREATED' AS '';

INSERT INTO Knowledge (Person, Difficulty, Theme) VALUE (0, 1, 1);

SELECT * FROM Knowledge;

CREATE TABLE Source (
	ID				INT UNSIGNED	NOT NULL AUTO_INCREMENT,
	PRIMARY KEY(ID),		#Here, we will have the course, articles, etc. that someone will need acording to his/her knowledge about theme
	Website				TEXT		,
	Theme				INT UNSIGNED	NOT NULL DEFAULT 0,
	Difficulty			INT UNSIGNED	NOT NULL DEFAULT 0
);

ALTER TABLE Source	ADD CONSTRAINT ResourceTheme 	FOREIGN KEY (Theme)	 	REFERENCES Theme(ID);
ALTER TABLE Source	ADD CONSTRAINT ResourceDiff	FOREIGN KEY (Difficulty)	REFERENCES Difficulty(ID);

SELECT 'SOURCE TABLE CREATED' AS '';

INSERT INTO Source (Website, Theme, Difficulty) VALUE ('localhost', 1, 1);

SELECT * FROM Source;

CREATE TABLE Question (
	ID				INT UNSIGNED 	NOT NULL AUTO_INCREMENT,
	PRIMARY KEY (ID),
	Text				TEXT		NOT NULL,
	Difficulty			INT UNSIGNED	,
	Theme				INT UNSIGNED	,
	Creator				INT UNSIGNED	NOT NULL,
	TotalAnswers			INT UNSIGNED	DEFAULT 0
);

ALTER TABLE Question 	ADD CONSTRAINT DifficultyMarker FOREIGN KEY (Difficulty) 	REFERENCES Difficulty(ID);
ALTER TABLE Question 	ADD CONSTRAINT ThemeMarker 	FOREIGN KEY (Theme) 		REFERENCES Theme(ID);
ALTER TABLE Question 	ADD CONSTRAINT QuestionCreator 	FOREIGN KEY (Creator)	 	REFERENCES Person(ID);

SELECT 'QUESTION TABLE CREATED' AS '';

INSERT INTO Question (Text, Difficulty, Theme, Creator, TotalAnswers) VALUE ('', 1, 1, 0, 0);

SELECT * FROM Question;

CREATE TABLE Answer (
	ID				INT UNSIGNED	NOT NULL AUTO_INCREMENT,
	PRIMARY KEY (ID),			#Storage of most frequent answer (taken as the correct one)
	Question			INT UNSIGNED	NOT NULL,
	Frequency			INT UNSIGNED	NOT NULL DEFAULT 1,
	Text				TEXT		NOT NULL
);

ALTER TABLE Answer	ADD CONSTRAINT QuestionRefer 	FOREIGN KEY (Question)	 	REFERENCES Question(ID);

SELECT 'ANSWER TABLE CREATED' AS '';

INSERT INTO Answer (Question, Frequency, Text) VALUE (1, 0, '');

SELECT * FROM Answer;
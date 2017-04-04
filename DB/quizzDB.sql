DROP DATABASE IF EXISTS quizDB;

CREATE DATABASE quizDB;

USE quizDB;

CREATE TABLE questions (
	QuestionID			INT UNSIGNED 	NOT NULL AUTO_INCREMENT,
	PRIMARY KEY (questionID),
	QuestionText			TEXT		NOT NULL,			
	Difficulty			INT UNSIGNED	NOT NULL DEFAULT 0,
	Theme				INT UNSIGNED	NOT NULL DEFAULT 0,						
	QuestionMaker			INT UNSIGNED	NOT NULL DEFAULT 0		
);

CREATE TABLE answers (
	ID				INT UNSIGNED	NOT NULL AUTO_INCREMENT,
	PRIMARY KEY (ID),		
	#Storage of most frequent answer (taken as the correct one)
	QuestionID			INT UNSIGNED	NOT NULL DEFAULT 0,
	AnswerText			TEXT		NOT NULL
);

CREATE TABLE theme (
	ID				INT UNSIGNED	NOT NULL AUTO_INCREMENT,	#Table of the different themes. Each theme can have a parent.
	PRIMARY KEY (ID),
	Label				TINYTEXT	NOT NULL,			#So we have a tree
	Parent				INT UNSIGNED	DEFAULT 0
);

CREATE TABLE difficulty(
	ID				INT UNSIGNED	NOT NULL AUTO_INCREMENT,
	PRIMARY KEY (ID),
	Difficulty			TINYTEXT	NOT NULL
);

CREATE TABLE users (
	ID				INT UNSIGNED	NOT NULL AUTO_INCREMENT,
	PRIMARY KEY (ID),
	TelegramID			INT UNSIGNED	NOT NULL DEFAULT 0
);

CREATE TABLE knowledge (
	ID				INT UNSIGNED	NOT NULL AUTO_INCREMENT,		#Storage of the knowledge of each user in a specific theme
	PRIMARY KEY(ID),
	UserID				INT UNSIGNED	NOT NULL DEFAULT 0,
	Difficulty			INT UNSIGNED	NOT NULL DEFAULT 0,
	Theme				INT UNSIGNED	NOT NULL DEFAULT 0
);

CREATE TABLE resources (
	ID				INT UNSIGNED	NOT NULL AUTO_INCREMENT,
	PRIMARY KEY(ID),		
#Here, we will have the course, articles, etc. that someone will need acording to his/her knowledge about theme
	ResourceSite			TEXT		NOT NULL,
	Theme				INT UNSIGNED	NOT NULL DEFAULT 0,
	Difficulty			INT UNSIGNED	NOT NULL DEFAULT 0
);

ALTER TABLE questions 	ADD CONSTRAINT DifficultyMarker FOREIGN KEY (Difficulty) 	REFERENCES difficulty(ID) 		ON UPDATE CASCADE;
ALTER TABLE questions 	ADD CONSTRAINT ThemeMarker 	FOREIGN KEY (Theme) 		REFERENCES theme(ID) 			ON UPDATE CASCADE;
ALTER TABLE questions 	ADD CONSTRAINT QuestionCreator 	FOREIGN KEY (QuestionMaker) 	REFERENCES users(ID) 			ON UPDATE CASCADE;
ALTER TABLE answers	ADD CONSTRAINT QuestionRefer 	FOREIGN KEY (QuestionID) 	REFERENCES questions(QuestionID) 	ON UPDATE CASCADE;
ALTER TABLE users 	ADD 				UNIQUE (TelegramID);
ALTER TABLE knowledge	ADD CONSTRAINT KnowledgeUser 	FOREIGN KEY (UserID)	 	REFERENCES users(ID)		 	ON UPDATE CASCADE;
ALTER TABLE knowledge	ADD CONSTRAINT KnowledgeDiff	FOREIGN KEY (Difficulty)	REFERENCES difficulty(ID)		ON UPDATE CASCADE;
ALTER TABLE knowledge	ADD CONSTRAINT KnowledgeTheme 	FOREIGN KEY (Theme)	 	REFERENCES theme(ID)		 	ON UPDATE CASCADE;
ALTER TABLE resources	ADD CONSTRAINT ResourceTheme 	FOREIGN KEY (Theme)	 	REFERENCES theme(ID)		 	ON UPDATE CASCADE;
ALTER TABLE resources	ADD CONSTRAINT ResourceDiff	FOREIGN KEY (Difficulty)	REFERENCES difficulty(ID)		ON UPDATE CASCADE;


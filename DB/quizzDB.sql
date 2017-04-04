CREATE DATABASE quizz;

CREATE TABLE questions ( 
	questionID		INT UNSIGNED 	NOT NULL AUTO_INCREMENT,
    questionNearID  INT UNSIGNED    NOT NULL DEFAULT 0,				#Questions with the same meaning or close to each other, will have the same questionNearID
	question		VARCHAR(1000)	NOT NULL DEFAULT '',			
	answer			VARCHAR(500)	NOT NULL DEFAULT '',
    difficulty		INT UNSIGNED	NOT NULL DEFAULT 0,				
	theme			INT UNSIGNED	NOT NULL DEFAULT 0,				
    questionMaker	INT UNSIGNED	NOT NULL DEFAULT '',			
	PRIMARY KEY (questionID),
    FOREIGN KEY (questionMaker) REFERENCES users (ID),
    FOREIGN KEY (theme) REFERENCES theme (ID),
    FOREIGN KEY (difficulty) REFERENCES difficulty (ID)
);
    
CREATE TABLE answers (
	ID				INT UNSIGNED	NOT NULL AUTO_INCREMENT,		#Storage of most frequent answer (taken as the correct one)
    question		INT UNSIGNED	NOT NULL DEFAULT 0,
    answer			VARCHAR(500)	NOT NULL DEFAULT '',
    PRIMARY KEY (ID),
    FOREIGN KEY (question) REFERENCES questions (questionNearID)	
);

CREATE TABLE theme (
	ID				INT UNSIGNED	NOT NULL AUTO_INCREMENT,		#Table of the different themes. Each theme can have a parent.
    label			VARCHAR(50)		NOT NULL DEFAULT '',			#So we have a tree
    parent			INT UNSIGNED	DEFAULT 0,
    PRIMARY KEY (ID)
);

CREATE TABLE difficulty(
	ID				INT UNSIGNED	NOT NULL AUTO_INCREMENT,
    difficulty		VARCHAR(50)		NOT NULL DEFAULT '',
    PRIMARY KEY (ID)
);

CREATE TABLE users (
	ID				INT UNSIGNED	NOT NULL AUTO_INCREMENT,
    telegramID		INT UNSIGNED	NOT NULL DEFAULT 0,
    PRIMARY KEY (ID)
);

ALTER TABLE users ADD UNIQUE (telegramID);

CREATE TABLE knowledge (
	ID				INT UNSIGNED	NOT NULL AUTO_INCREMENT,		#Storage of the knowledge of each user in a specific theme
	user			INT UNSIGNED	NOT NULL DEFAULT 0,
    difficulty		INT UNSIGNED	NOT NULL DEFAULT 0,
    theme			INT UNSIGNED	NOT NULL DEFAULT 0,
    PRIMARY KEY(ID),
    FOREIGN KEY (user) REFERENCES users (ID),
    FOREIGN KEY (difficulty) REFERENCES difficulty (ID),
    FOREIGN KEY (theme) REFERENCES theme(ID)
);

CREATE TABLE resources(
	ID				INT UNSIGNED	NOT NULL AUTO_INCREMENT,		#Here, we will have the course, articles, etc. that someone will need acording to his/her knowledge about theme
    resourceSite	VARCHAR(500)	NOT NULL DEFAULT '',
    theme			INT UNSIGNED	NOT NULL DEFAULT 0,
    difficulty		INT UNSIGNED	NOT NULL DEFAULT 0,
    PRIMARY KEY(ID),
    FOREIGN KEY(theme) REFERENCES theme (ID),
    FOREIGN KEY(difficulty) REFERENCES difficulty (ID)
);
    

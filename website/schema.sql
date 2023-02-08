CREATE TABLE users(user_id VARCHAR(50) NOT NULL,password VARCHAR(30) NOT NULL,email VARCHAR(60),PRIMARY KEY(user_id));


CREATE TABLE Leaderboard(user_id VARCHAR(50) NOT NULL,High_score INT NOT NULL,PRIMARY KEY(user_id));


SELECT * from Leaderboard


INSERT INTO Leaderboard VALUES("user6",1500)

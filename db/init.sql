CREATE DATABASE bingo;
USE bingo;

CREATE TABLE users (
	UserName VARCHAR(50),
	Password VARCHAR(64)
);

INSERT INTO users
	(UserName, Password)
VALUES
	("admin", "toor"),
	("Rune", "enur");
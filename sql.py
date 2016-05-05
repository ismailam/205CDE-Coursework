import sqlite3


with sqlite3.connect("sample.db") as connection:
	c = connection.cursor()
	c.execute(""" CREATE TABLE user(firstName VARCHAR, lastName VARCHAR, email VARCHAR, password VARCHAR )""")
	c.execute('INSERT INTO user VALUES("Abba", "Kwais", "ismailam@uni.coventry", "38055322")')
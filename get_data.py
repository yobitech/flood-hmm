#!/usr/bin/python

import MySQLdb

# open database connection
db = MySQLdb.connect('localhost', 'testuser', 'test123', 'TESTDB')

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method
cursor.execute("SELECT VERSION()")

# fetch a single row using fetchone() method
data = cursor.fetchone()

# disconnect from server
db.close()
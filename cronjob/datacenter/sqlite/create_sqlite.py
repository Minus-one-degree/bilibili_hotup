# -*- coding: utf-8 -*-

import sqlite3

conn = sqlite3.connect('test_bilibili.db')
print ("Opened database successfully")
c = conn.cursor()
c.execute('''CREATE TABLE HOTUP
       (id integer primary key autoincrement,
       avnumber       CHAR(50)  NOT NULL,
       title         CHAR(50)   NOT NULL,
       length       DATE        NOT NULL,
       playtime        INT,
       subtitle      INT,
       date          DATE       NOT NULL,
       upname      CHAR(50)     NOT NULL,
       time         DOUBLE     NOT NULL);''')
print ("Table created successfully")
conn.commit()
conn.close()
#!/usr/bin/env python3

import os
import os.path
import sys
import sqlite3 as sql
from datetime import datetime, date, time

DB_NAME = 'reminder_db.db'
conn = sql.connect(DB_NAME)
cursor = conn.cursor() 
while True:
	current_date = str(datetime.now()).split('.')[0][:-3].strip()
	cursor.execute("SELECT *FROM reminder")
	data = cursor.fetchall()
	for each in data:
		if(str(each[3]).split('.')[0][2:18].strip() == current_date):
			os.system('notify-send "Today Reminder: '+each[0]+'"')
		else:
			pass

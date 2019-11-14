#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Goldy T Joseph
# Mail: goldythundiyiljoseph@gmail.com
# Remind Me is a reminder application.


import os
import sys
import sqlite3 as sql
from datetime import datetime, date, time


# Make sqlite3 database connection
DB_NAME = 'reminder_db.db'
CONN = sql.connect(DB_NAME)
cursor = CONN.cursor()


# Banner
def banner():
	print(r'''
	88''Yb 888888 8b    d8 88 88b 88 8888b.  888888 88''Yb 
	88__dP 88__   88b  d88 88 88Yb88  8I  Yb 88__   88__dP 
	88''Yb 88''   88YbdP88 88 88 Y88  8I  dY 88''   88''Yb  
	88  Yb 888888 88 YY 88 88 88  Y8 8888Y'  888888 88  Yb 
	''')

		
# If a table donot exist then, creates a table and if exist then wont overwrite
def createTable():
	cursor.executescript('''
		CREATE TABLE IF NOT EXISTS reminder (
    	id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    	title TEXT,
		create_date TEXT,
		remind_date TEXT);
		''')


# Function for data insertion 
def insertRemind(rem_name, rem_date):
	cursor.execute('''INSERT OR IGNORE INTO reminder (
		title, create_date, remind_date) 
        VALUES ( ?, ?, ? )''', ( rem_name, str(datetime.now()).split('.')[0], rem_date)) 
	CONN.commit()


# Reminder creation function
def createReminder():
	os.system('clear')
	current_year = datetime.now().year	
	remind_content = input('Reminder about: ')
	remind_year = input('Set reminder at (year, eg. 2019)?: ')
	if int(remind_year) < current_year:
		input('This is not valid because the year less current year...! [Press ENTER]')
		updateReminder()
	remind_month = input('In which month (eg. 1-12)? ')
	if int(remind_month) > 12:
		input('This selection is not valid...! [Press ENTER]')
		updateReminder()
	remind_day = input('On which day (eg. 1-31)? ')
	if int(remind_day) > 31:
		input('This selection is not valid...! [Press ENTER]')
		updateReminder()
	remind_hour = input('Hour (eg. 1-12)? ')
	remind_mind = input('Minute (eg. 0-59)? ')
	# get full date like year, month, day
	full_date = date(int(remind_year), int(remind_month), int(remind_day))
	# get the full time like hour and minutes
	full_time = time(int(remind_hour), int(remind_mind))
	# combined date and time 
	combined_date = datetime.combine(full_date, full_time)
	print('Reminder added for:',combined_date)
	print('Created at',str(datetime.now()))
	insertRemind(remind_content, combined_date)


#For viewing and deleting (specific reminder)
def viewRemind(rec=0):
	if rec == 0:
		os.system('clear')
		cursor.execute('SELECT *FROM reminder')
		data = cursor.fetchall()
		print('{0:5} {1:20} {2:25} {3:5} '.format('|id|', '|title|', '|   created date  |',
				'|   remind date   |'))
		print('{0:5} {1:20} {2:25} {3:5} '.format('-'*4, '-'*7, '-'*19, '-'*19))
		for item in data:
			print('{0:5} {1:20} {2:25} {3:5} '.format(str(item[0]), item[1], item[2], item[3]))	
	else:
		os.system('clear')
		cursor.execute('DELETE FROM reminder WHERE id = ?', (rec, ))
		CONN.commit()
		cursor.execute('SELECT *FROM reminder')
		data = cursor.fetchall()
		print('{0:5} {1:20} {2:25} {3:5}'.format('|id|', '|title|', '|created date|', '|remind date|'))
		print('{0:5} {1:20} {2:25} {3:5} '.format('-'*4, '-'*7, '-'*19, '-'*19))
		for item in data:
			print('{0:5} {1:20} {2:25} {3:5} '.format(item[0], item[1], item[2], item[3]))


# Updation of TASKS already exist
def updateReminder():
	#os.system('clear')
	current_year = datetime.now().year
	print('DONT NEED TO UPDATE ??? ')
	task_id = input('TASK U NEED TO UPDATE (ID) ')
	if int(task_id) == -99:
		main()
	viewRemind()
	print('\n{0:~^20s}'.format('Update section'))
	remind_content = input('What you want to remind? ')
	remind_year = input('When you get reminded (year, eg. 2018)? ')
	if int(remind_year) < current_year:
		input('This is not valid because the year less current year...! [Press ENTER]')
		updateReminder()
	remind_month = input('In which month (eg. 1-12)? ')
	remind_day = input('On which day (eg. 1-31)? ')
	remind_hour = input('Hour (eg. 1-12)? ')
	remind_mind = input('Minute (eg. 0-59)? ')
	full_date = date(int(remind_year), int(remind_month), int(remind_day))
	full_time = time(int(remind_hour), int(remind_mind))
	combined_date = datetime.combine(full_date, full_time)
	cursor.execute('''UPDATE reminder 
					SET title = ?,
					create_date = ?,
					remind_date = ? 
					WHERE id =?''',
					(remind_content, 
						str(datetime.now()).split('.')[0],
						combined_date,
						task_id)) 
	CONN.commit()
		
def main():
	createTable()
	banner()
	while True:
		print(r'''
CREATE		UPDATE		DELETE		VIEW		EXIT
press 0		press 1		press 2		press 3		press 4
		''')
		choice = input('>>> ')
		try:
			if int(choice) < 0: pass
			elif int(choice) == 0:
				createReminder()
			elif int(choice) == 1:
				updateReminder()
			elif int(choice) == 2:
				viewRemind(0)
				viewRemind(input('Reminder need to be deleted (ID)'))
			elif int(choice) == 3:
				viewRemind(0)
				main()
			elif int(choice) == 4:
				sys.exit(0)
			else:
				pass
		except ValueError:
			print('Invalid option')
			os.system('clear')
		except IndexError:
			print('Out of index')
			os.system('clear')
		except KeyboardInterrupt:
			print('\n')
			sys.exit(0)

if __name__ == '__main__':
	main()

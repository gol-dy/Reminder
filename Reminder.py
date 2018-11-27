#!/usr/bin/env python3
#Author: Goldy T Joseph
#Mail: goldythundiyiljoseph@gmail.com
#Remind Me is a python program which works like a reminder application.
#
import os
import os.path
import sys
import sqlite3 as sql
import subprocess
from datetime import datetime, date, time

# Make sqlite3 database connection
DB_NAME = 'reminder_db.db'
conn = sql.connect(DB_NAME)
cursor = conn.cursor()

# Header
header = """
  _____  ______ __  __ _____ _   _ _____    __  __ ______   ___   
 |  __ \|  ____|  \/  |_   _| \ | |  __ \  |  \/  |  ____| |__ \  
 | |__) | |__  | \  / | | | |  \| | |  | | | \  / | |__       ) | 
 |  _  /|  __| | |\/| | | | | . ` | |  | | | |\/| |  __|     / /  
 | | \ \| |____| |  | |_| |_| |\  | |__| | | |  | | |____   |_|   
 |_|  \_\______|_|  |_|_____|_| \_|_____/  |_|  |_|______|  (_)   
                                                                  
                                                                  
"""

menu = """ CREATE		UPDATE		DELETE		VIEW		EXIT
 press 0	press 1		press 2		press 3		press 4 
		"""

		
# If a table donot exist then, creates a table and if exist then wont overwrite
def create_table():
	cursor.executescript("""
		CREATE TABLE IF NOT EXISTS reminder (
    	id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    	title    TEXT,
		create_date TEXT,
		remind_date TEXT);
		""")

# Function for data insertion 
def insert_remind(rem_name, rem_date):
	cursor.execute('''INSERT OR IGNORE INTO reminder (
		title, create_date, remind_date) 
        VALUES ( ?, ?, ? )''', ( rem_name, str(datetime.now()).split('.')[0], rem_date)) 
	conn.commit()
	main_menu()
# Reminder creation function
def create_reminder():
	os.system('clear')
	current_year = datetime.now().year	
	remind_content = input('About what I need to remind you? ')
	remind_year = input('When you get reminded (year, eg. 2018)? ')
	if int(remind_year) < current_year:
		input("This is not valid because the year less current year...! [Press ENTER]")
		update_reminder()
	remind_month = input('In which month (eg. 1-12)? ')
	remind_day = input('On which day (eg. 1-31)? ')
	remind_hour = input('Hour (eg. 1-12)? ')
	remind_mind = input('Minute (eg. 0-59)? ')
	# get full date like year, month, day
	full_date = date(int(remind_year), int(remind_month), int(remind_day))
	# get the full time like hour and minutes
	full_time = time(int(remind_hour), int(remind_mind))
	# combined date and time 
	combined_date = datetime.combine(full_date, full_time)
	print("Reminder added for:",combined_date)
	print("Created at",str(datetime.now()))
	insert_remind(remind_content, combined_date)
	main_menu()
#For viewing and deleting (specific reminder)
def view_remind(rec=0):
	if rec == 0:
		os.system('clear')
		cursor.execute("SELECT *FROM reminder")
		data = cursor.fetchall()
		print("{0:5} {1:20} {2:25} {3:5} ".format("|id|", "|title|", "|created date     |",
				"|remind date      |"))
		print("{0:5} {1:20} {2:25} {3:5} ".format("-"*4, "-"*7, "-"*19, "-"*19))
		for item in data:
			print("{0:5} {1:20} {2:25} {3:5} ".format(str(item[0]), item[1], item[2], item[3]))
		
	else:
		os.system('clear')
		cursor.execute("DELETE FROM reminder WHERE id = ?", (rec, ))
		conn.commit()

		cursor.execute("SELECT *FROM reminder")
		data = cursor.fetchall()
		
		print("{0:5} {1:20} {2:25} {3:5}".format("|id|", "|title|", "|created date|", "|remind date|"))
		print("{0:5} {1:20} {2:25} {3:5} ".format("-"*4, "-"*7, "-"*19, "-"*19))
		for item in data:
			print("{0:5} {1:20} {2:25} {3:5} ".format(item[0], item[1], item[2], item[3]))
		main_menu()
# Updation of TASKS already exist
def update_reminder():
	#os.system('clear')
	current_year = datetime.now().year
	print("DONT NEED TO UPDATE ??? ")
	task_id = input("TASK U NEED TO UPDATE (ID) ")
	if int(task_id) == -99:
		main_menu()
	view_remind()
	print("\n{0:~^20s}".format("Update section"))
	remind_content = input('What you want to remind? ')
	remind_year = input('When you get reminded (year, eg. 2018)? ')
	if int(remind_year) < current_year:
		input("This is not valid because the year less current year...! [Press ENTER]")
		update_reminder()
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
	conn.commit()
	main_menu()
# Dict of CLI menu_items
menuItems = [
    { "Create reminder": 0 },
    { "Update reminder": 1 },
	{ "Delete specific": 2 },
    { "View all": 3 },
	{ "Exit": 4 },
]
			
def main_menu():                                
	while True:
		#os.system('clear')
		print(header,"\n")
		print(menu,"\n")

		choice = input(">>> ")
		try:
			if int(choice) < 0: pass
			elif int(choice) == 0:
				create_reminder()

			elif int(choice) == 1:
				update_reminder()

			elif int(choice) == 2:
				view_remind(0)
				view_remind(input("What I need to forget ? ENTER ID"))

			elif int(choice) == 3:
				view_remind(0)
				main_menu()

			elif int(choice) == 4:
				sys.exit(0)
			else:
				pass
		except ValueError:
			print("Invalid option")
			os.system('clear')
		except IndexError:
			print("Out of index")
			os.system('clear')

if __name__ == '__main__':
	
	subprocess.call(["bash", "run.sh"])
	create_table()
	main_menu()
	



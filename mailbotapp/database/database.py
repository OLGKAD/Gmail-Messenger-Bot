###################  Set UP #########################

from flask import Flask, render_template, request
from werkzeug import generate_password_hash, check_password_hash
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()

#MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'gmailbot'
app.config['MYSQL_DATABASE_DB'] = 'mailbot'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_CHARSET']='utf8mb4'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()


def get_unsent_emails():
    cursor.callproc('get_unsent_emails', args=())
    data = cursor.fetchall()
    conn.commit()
    return data   # then rows in data can be accessed as "for row in data: <do smth>"		

# after unsent emails have been fetched, it updates their statuses to "sent"
def update_email_stats():    
    cursor.callproc('update_email_stat', args=())
    data = cursor.fetchall()
    conn.commit()

# get a list of users with FB ids and tokens from the tbl_users
def get_users():
    cursor.callproc('get_users', args=())
    data = cursor.fetchall()
    conn.commit()
    return data

def add_email(email): # email - tuple of arguments	
	cursor.callproc('add_email', email)
	data = cursor.fetchall()
	conn.commit()	

def add_user(FB_id, token, user_photo, name): # FB_id - int, token - JSON
    cursor.callproc('add_user', (FB_id, token, user_photo, name, 0))
    data = cursor.fetchall()
    conn.commit()

# returns true if a user with a given FB_id exists
def user_exists(FB_id):
    args = [FB_id]
    cursor.callproc('user_exists', args)
    data = cursor.fetchone()
    if (data[0] == 0):
	return False
    else: 
	return True

def get_FB_id(user_id):
    args = [user_id]
    cursor.callproc('get_FB_id',args)
    data = cursor.fetchone()
    return data[1]

def get_user_photo(user_id):
    args = [user_id]
    cursor.callproc('get_FB_id',args)
    data = cursor.fetchone()
    conn.commit()
    return data[3]

def get_user_name(user_id): 
    args = [user_id]
    cursor.callproc('get_FB_id',args)
    data = cursor.fetchone()
    conn.commit()
    return data[4]

def get_user_id(FB_id):
	args = [FB_id]
	cursor.callproc('get_user_id', args)
	data = cursor.fetchone()
	return data[0]

def get_user(FB_id):
    user_id = get_user_id(FB_id)
    print(user_id)
    args = [user_id]
    cursor.callproc('get_FB_id', args)
    data = cursor.fetchone()
    return data

def get_email(email_id):
	args = [email_id]
	cursor.callproc('get_email', args)
	data = cursor.fetchone()
	conn.commit()
	return data

# given user_id and sender_id, it fetches all old emails previously sent to the given user by the given recipient 
def get_old_emails(user_id, sender_id):
    args = [user_id, sender_id]
    cursor.callproc('get_old_emails', args)
    data = cursor.fetchall()
    return data

      

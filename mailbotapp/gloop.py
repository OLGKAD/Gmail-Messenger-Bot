if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        from mbot import Mbot
        from gbot import Gbot
    else:
        from .mbot import Mbot  
        from .gbot import Gbot
gbot = Gbot()
mbot = Mbot()
import pymysql
import json
import time
import socket
from database.database import *
sys.setdefaultencoding('utf-8')

emails_raw = None
users = get_users()
users_list = []
for user in users:
    tmp = []
    tmp.append(user[0])
    tmp.append(user[1])
    tmp.append(user[2])
    tmp.append(time.time())
    users_list.append(tmp)

while True:
    for user in users_list:
        user_id = user[0]
        #print(user)
        psid = user[1]
       # print psid
        creds = mbot.credentials_from_dict(json.loads(user[2]))
        try:
            gmail = gbot.access_gmail(creds)
            emails_raw,user[3] = gbot.get_emails(user[3])
            print(emails_raw)
        except socket.timeout:
            with open("test.logs", "w") as f:
                f.write("Time: " + str(time.time()) +" " + str(user_id)+'\n')
            continue
        except:
            continue
        
        for email_raw in emails_raw:
            print (email_raw)
            subject = gbot.get_subject(email_raw)
            sender_name, sender_email = gbot.get_sender(email_raw)
            body,withAtt = gbot.get_body(email_raw)
            attachments_data = []
            if withAtt:
                print('getting attachments')
                attachments_path = gbot.get_attachments(email_raw, psid)
                print('att path: ',attachments_path) 
            else:
                attachments_path = '' 
            date = gbot.get_date(email_raw)
            try:
                photo = gbot.get_photo(sender_email)
            except ValueError:
                photo = "https://library.lanecc.edu/sites/default/files/staff/User_0_2.png"
            #photo = 'photo.jpg'
        
            email = (user_id,sender_email, subject, sender_name, body, date, 0,photo,-1, attachments_path)
            #print(email)
            try:
                add_email(email)
            except pymysql.err.InternalError:
                add_email((user_id,sender_email, 'Error', "MailBot", 'Currently only English is supported. Most probably this emails contained symbols from other languages.', date, 0, photo, -1, attachments_path))
    '''   
    # Update users_list
    users = get_users()
    #users_list = []
    users_list_new = []
    for user in users:
        user_tmp = filter(lambda x:x[1]==user[1], users_list)
        #print(user_tmp)
        if user_tmp:
           # print('here')
            #ind = users_list.index(user_tmp)
            users_list_new.append(user_tmp[0])
        else:
            #print('not here')
            tmp = []
            tmp.append(user[0])
            tmp.append(user[1])
            tmp.append(user[2])
            tmp.append(time.time())
            users_list_new.append(tmp)
    #print(users_list)
    #print(users_list_new)
    users_list = users_list_new
    # Sleep 1 second to avoid problems with database
    #time.sleep(1)
    '''
    mbot.send_unsent_emails()

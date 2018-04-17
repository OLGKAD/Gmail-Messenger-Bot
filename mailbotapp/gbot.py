# -*- coding: utf-8 -*-
from __future__ import print_function
import httplib2
from email.MIMEMultipart import MIMEMultipart
import os
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
from werkzeug.utils import secure_filename
from googleapiclient.discovery import build
from database.database import *
import base64
import urllib
import re
from bs4 import BeautifulSoup
from mbot import Mbot
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import time
from email.utils import parsedate_tz, mktime_tz, formatdate
import json
class Gbot(object):
    def __init__(self):
        self.gmail = None
    
    def access_gmail(self,credentials):
        self.gmail = build('gmail', 'v1', credentials=credentials, cache_discovery=False)
    def get_emails(self, after_time):
        query = 'is:unread AND after:%d'%(after_time)
        threads = self.gmail.users().messages().list(userId='me', q = query).execute()
        print('threads: ', threads)
        emails = []
        if not 'messages' in threads:
            return emails, time.time()
        while 'nextPageToken' in threads:
            page_token = threads['nextPageToken']
            threads.extend(self.gmail.users().messages().list(userId='me', q = query, pageToken = page_token).execute())
        for email in threads['messages']:
            msg_id = email['id']
            email_det = self.gmail.users().messages().get(userId='me',id=msg_id).execute()  
            print('email_det', email_det)
            emails.append(email_det)
        return emails, time.time()

    def get_subject(self,email):
        for header in email['payload']['headers']:
            if header['name']=='Subject':
                return header['value']
    def get_sender(self,email):
        for header in email['payload']['headers']:
            if header['name']=='From':
                if '<' in header['value']:
                    tmp = header['value'].split('<')
                    name = tmp[0].strip()
                    email = tmp[1].split('>')[0].strip()
                else:
                    name = header['value']
                    email = header['value']
                return name, email

    def get_body(self, email):
        withAtt=False
        if email['payload']['mimeType']=='multipart/mixed':
            withAtt = True
        text = ''
        if not any(d['name']=='X-Received' for d in email['payload']['headers']): 
            mssg_parts = email['payload']['parts'] # fetching the message parts
            if not any(d.get('parts',None) for d in mssg_parts):
                for part in mssg_parts:
                    if part['mimeType']=='text/plain':
                        part_one=part
                        part_body = part_one['body'] # fetching body of the message
                        part_data = part_body['data'] # fetching data from the body
                        clean_one = part_data.replace("-","+") # decoding from Base64 to UTF-8
                        clean_one = clean_one.replace("_","/") # decoding from Base64 to UTF-8
                        clean_two = base64.b64decode (bytes(clean_one)) # decoding from Base64 to UTF-8
                        text = clean_two
            else:
                for d in mssg_parts:    
                    if 'parts' in d:
                        parts = d['parts']
                for part in  parts:
                    if part['mimeType']=='text/plain':
                        part_one=part
                        part_body = part_one['body'] # fetching body of the message
                        part_data = part_body['data'] # fetching data from the body
                        clean_one = part_data.replace("-","+") # decoding from Base64 to UTF-8
                        clean_one = clean_one.replace("_","/") # decoding from Base64 to UTF-8
                        clean_two = base64.b64decode (bytes(clean_one)) # decoding from Base64 to UTF-8
                        text = clean_two

        else: 
            if 'parts' in email['payload']:
                mssg_parts = email['payload']['parts'] # fetching the message parts
                for part in mssg_parts:
                    if part['mimeType']=='text/plain':
                         part_one=part
                         part_body = part_one['body'] # fetching body of the message
                         part_data = part_body['data'] # fetching data from the body
                         clean_one = part_data.replace("-","+") # decoding from Base64 to UTF-8
                         clean_one = clean_one.replace("_","/") # decoding from Base64 to UTF-8
                         clean_two = base64.b64decode (bytes(clean_one)) # decoding from Base64 to UTF-8
                         text = clean_two     
            else:
                part_data = email['payload']['body']['data']
                clean_one = part_data.replace("-","+") # decoding from Base64 to UTF-8
                clean_one = clean_one.replace("_","/") # decoding from Base64 to UTF-8
                clean_two = base64.b64decode (bytes(clean_one)) # decoding from Base64 to UTF-8
                text = clean_two
        return text,withAtt
    
    #OUTPUT:[(file_name, byte_data),(..)...]       
    def get_attachments(self,email,user_psid):
        msg_id = email['id']
        
        msg = self.gmail.users().messages().get(userId='me', id = msg_id).execute()
        files_path =''
        for part in msg['payload']['parts']:
            newvar = part['body']
            if 'attachmentId' in newvar:      
                att_id = newvar['attachmentId']
                att = self.gmail.users().messages().attachments().get(userId='me', messageId=msg_id, id=att_id).execute()
                data = att['data']
                file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                file_name = secure_filename(part['filename'])
                file_name = str(user_psid)+'_'+str(time.time())+'_'+file_name
                file_path = '/var/www/mailbotapp/uploads/'
                path = ''.join([file_path, file_name])
                #file_data.save(file_path)
                with open(path, 'w') as f:
                    f.write(file_data)
               
                files_path = files_path + file_name + ';'
        return files_path
        
    def get_photo(self, email_addr):
        url = 'http://picasaweb.google.com/data/entry/api/user/'+email_addr+'?alt=json'
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        photo = data['entry']['gphoto$thumbnail']['$t']
        return photo
    def get_date(self, email):
        
        for header in email['payload']['headers']:
              if header['name']=='Date':
                  date_str = str(header['value'])
                  tt = parsedate_tz(date_str)
                  #timestamp = mktime_tz(tt)
                  (2017, 11, 27, 22, 29, 35, 0, 1, -1, 32400)
                  date =str(tt[0])+'-'+str(tt[1])+'-'+str(tt[2])+' '+str(tt[3])+':'+str(tt[4])+':'+str(tt[5])
                  return date
    
    def send_email(self,sender_psid, receiver_email,subject, email_text, attachment=None):
        mbot = Mbot()
        sender = get_user(sender_psid)
        sender_token = mbot.credentials_from_dict(json.loads(sender[2]))
        self.access_gmail(sender_token)
        message = MIMEMultipart()
        message['To']= receiver_email
        info = self.gmail.users().getProfile(userId='me').execute()
        name = mbot.get_user_name(sender[0])
        email = info['emailAddress']
        message['From'] = name + ' <'+email+'>'
        message['Subject'] = subject
        message.attach(MIMEText(email_text, 'plain'))
        #attachment = '/var/www/mailbotapp/mailbotapp/token.json'
        if not attachment==None:
            att_name = os.path.split(attachment)[1]
            att_file = open(attachment, 'rb')
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((att_file).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % att_name)
            message.attach(part)
        email = {'raw': base64.urlsafe_b64encode(message.as_string())}
        self.gmail.users().messages().send(userId='me', body=email).execute()      

I. Introduction. 

This is a Facebook Messenger Bot. It lets people who have Gmail and FB accounts to both receive and reply to their emails in the FB Messenger app, just like they would do it with FB messages. 


II. Setup Instructions.

1. Current files should be located in /var/www/mailbotapp directory

2. You also need to add /etc/apache2/sites-available/mailbotapp.conf file with following contents:
<VirtualHost *:6680>
                ServerName localhost
		ServerAlias *.ngrok.io
                ServerAdmin t.b.alisher@gmail.com
                WSGIScriptAlias / /var/www/mailbotapp/mailbotapp.wsgi
                <Directory /var/www/mailbotapp/mailbotapp/>
                        Require all granted
                </Directory>
                Alias /static /var/www/mailbotapp/mailbotapp/static
                <Directory /var/www/mailbotapp/mailbotapp/static/>
                        Require all granted
                </Directory>
                ErrorLog ${APACHE_LOG_DIR}/error.log
                LogLevel warn
                CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost> 


III. File strutcture. 

Most important files: 
1. The "database" folder contains MySQL functions, and "database.py" - a python API for interactions with the DB. 
2. "gbot.py" - for interactions with the Gmail end using Gmail API.
3. "__init__.py" - uses Flask to handle the communications with the client side (FB Messenger and the web-form).
4. "mbot.py" -  serves as a middleware between "database.py" and "__init__.py". 

IV. Credits. 

The code was written and developed by me (Olzhas Kadyrakunov), Alisher Tortay and Yekaterina Abileva. Roughly, Kate was responsible for the Gmail end of the system, I was responsible for the "middle part" (interactions with the database), and Alisher was responsible for the FB Messenger end. 
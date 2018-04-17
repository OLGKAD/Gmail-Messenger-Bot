#!/usr/bin/python2.7
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/mailbotapp/")

from mailbotapp import app as application
application.secret_key = 'Add your secret key'

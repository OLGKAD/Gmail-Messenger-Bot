# -*- coding: utf-8 -*-
from __future__ import print_function
import flask
import requests
import json
from .mbot import Mbot
from .gbot import Gbot
from werkzeug.utils import secure_filename
from .forms import ChatForm, NewEmailForm
import os
import time
from datetime import datetime
# TODO: make it work with https 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = flask.Flask(__name__)

mbot = Mbot()
gbot = Gbot()


@app.route('/', methods=['GET'])
def handle_verification():
    if flask.request.args['hub.verify_token'] == mbot.VERIFY_TOKEN:
        return flask.request.args['hub.challenge']
    else:
        return "Invalid verification token"


@app.route('/', methods=['POST'])
def handle_incoming_messages():
    data = flask.request.json
    sender = data['entry'][0]['messaging'][0]['sender']['id']
    messagingArray = data['entry'][0]['messaging'][0]
    if messagingArray.has_key('postback'):
        if messagingArray['postback']['payload'] == 'GET_STARTED_PAYLOAD':
            mbot.send_text(sender, 'Hello there!')
    if not mbot.check_authorized(sender):
        auth_url = flask.url_for('authorize', user_psid=sender, _external=True)
        mbot.send_login_button(sender, auth_url)
    else:
        mbot.send_instructions(sender)
        mbot.send_unsent_emails()
    return "ok"


@app.route('/authorize/<int:user_psid>')
def authorize(user_psid):
    if mbot.check_authorized(user_psid):
        return "You have already authorized."
    redirect_uri = flask.url_for('oauth2callback', _external=True)
    authorization_url, state = mbot.authorize(redirect_uri)
    # Store the state so the callback can verify the auth server response.
    flask.session['state'] = state
    flask.session['user_psid'] = user_psid
    return flask.redirect(authorization_url)


@app.route('/oauth2callback')
def oauth2callback():
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = flask.session['state']
    user_psid = flask.session['user_psid']
    redirect_uri = flask.url_for('oauth2callback', _external=True)
    authorization_response = flask.request.url
    # get user profile (name, photo) from Facebook
    user_profile = json.loads(requests.get("https://graph.facebook.com/v2.6/{psid}?fields=first_name,last_name,profile_pic&access_token={token}".format(psid=user_psid, token=mbot.ACCESS_TOKEN)).content)
    credentials = mbot.oauth2callback(user_psid, user_profile, state, redirect_uri, authorization_response)
    return 'Authorization is complete.'

    
@app.route('/chat/<int:user_psid>/<int:email_id>', methods=['GET', 'POST'])
def chat(user_psid, email_id):
    # TODO: make it secure
    form = ChatForm()
    email = mbot.get_email(email_id)
    sender_name = email[4]
    user_id, sender_id = mbot.get_user_id_and_sender_id_from_email_id(email_id)
    conv_body = mbot.get_old_emails(user_id, sender_id)
    if flask.request.method == 'POST':
        if form.validate() is False:
            flask.flash('All fields are required.')
            return flask.render_template('reply.html', form=form, sender_name=sender_name, conv_body=conv_body, action_url=flask.url_for('chat', user_psid=user_psid,
                                                                                   email_id=email_id, _external=True))
        else:
            attach = form.attachment.data
            filename = None
            full_filename = None
            print(attach)
            if attach is not None:
                filename = secure_filename(attach.filename)
                filename = str(user_psid) + '_' + str(time.time()) + '_' + filename
                full_filename = '/var/www/mailbotapp/uploads/' + filename
                attach.save(full_filename)
            user_photo = mbot.get_user_photo(email[1])
            user_name = mbot.get_user_name(email[1])
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            mbot.create_email(email[1], email[2], email[3], user_name, form.message.data, date, 1, user_photo,  1, filename)
            gbot.send_email(user_psid, email[2], email[3], form.message.data, full_filename)
            return flask.render_template('reply.html', success=True, _external=True)
    return flask.render_template('reply.html', form=form, sender_name=sender_name, conv_body=conv_body, action_url=flask.url_for('chat', user_psid=user_psid, email_id=email_id, _external=True))


@app.route('/newEmail/<int:user_psid>', methods=['GET', 'POST'])
def newEmail(user_psid):
    form = NewEmailForm()
    if flask.request.method == 'POST':
        if form.validate() is False:
            flask.flash('All fields are required.')
            return flask.render_template('new_email.html', form=form,
                                         action_url=flask.url_for('newEmail', user_psid=user_psid, _external=True))
        else:
            attach = form.attachment.data
            filename = None
            full_filename = None
            if attach is not None:
                filename = secure_filename(attach.filename)
                filename = str(user_psid) + '_' + str(time.time()) + '_' + filename
                full_filename = '/var/www/mailbotapp/uploads/' + '_' + filename
                attach.save(full_filename)
            user_id = mbot.get_user_id(user_psid)
            user_photo = mbot.get_user_photo(user_id)
            user_name = mbot.get_user_name(user_id)
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            mbot.create_email(user_id, form.email.data, form.subject.data, user_name, form.message.data, date, 1, user_photo, 1, filename)
            gbot.send_email(user_psid, form.email.data, form.subject.data, form.message.data, full_filename)
            return flask.render_template('new_email.html', success=True, _external=True)
    return flask.render_template('new_email.html', form=form,
                                 action_url=flask.url_for('newEmail', user_psid=user_psid, _external=True))


@app.route('/attachment/<path:path>', methods=['GET'])
def get_attachment(path):
    return flask.send_from_directory('/var/www/mailbotapp/uploads/', path, as_attachment=True)

if __name__ == "__main__":
    app.run()


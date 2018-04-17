from flask import Flask, render_template, request
from werkzeug import generate_password_hash, check_password_hash
from flask.ext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()

#MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'gmailbot'
app.config['MYSQL_DATABASE_DB'] = 'mailbot'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route("/")
def main():
    conn1 = mysql.connect()
    cursor1 = conn1.cursor()
    conn2 = mysql.connect()
    cursor2 = conn2.cursor()
    #_hashed_password = generate_password_hash(_password)
    cursor1.callproc('add_user',('Olzhas','cool@gmail.com','token','refresh_token','token_uri','client_id','client_secret','scopes',101,'Olzhas Kadyrakun'))

    ## add_email is disabled for now, since foreign key constrains cannot be satisfied (but the function works): 
    ## users are added with ever increamenting ids (1, .., 8, ..), but emails are added with a fixed id, or with ids changing idependently

    #cursor2.callproc('add_email',(1,1,'meeting',"Kate","what's up madafaka?",'2017-10-29 17:45:40'))
    #conn2.commit() # should be commited after add_user due to foreign key constrains
    data = cursor1.fetchall()
    if len(data) is 0:
       conn1.commit()
     #  conn2.commit()
       return "data has been successfully added!"
    else:
      # conn2.commit()
       return "data hasn't been added"


if __name__ == "__main__":
    app.run()

from flask import Flask, request, render_template
from flask import jsonify, make_response

import DB 

from flask_mysqldb import MySQL
import smtplib

import slack
import os
from pathlib import Path
from dotenv import load_dotenv

app= Flask(__name__)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "Password"
app.config['MYSQL_DB'] = "usertest"

env_path =  Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

mysql = MySQL(app)

'''
#the below email/slack functions taken in creds from .env file
'''

def emailnotification(message):

        from_email=os.environ['FROM_MAIL']
        from_email_pwd=os.environ['FROM_MAILPWD']
        to_email=os.environ['TO_MAIL']
        server= smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(from_email,from_email_pwd)
        server.sendmail(from_email,to_email,message)

def slacknotification(message):
        client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
        client.chat_postMessage(channel='#test',text=message)



@app.route("/user/registration", methods=["POST"])
def json_example():

    if request.is_json:

            req = request.get_json()
            '''
            try:
               slacknotification(req)
           
            except:
                return make_response(jsonify({"message": "Unable to send to slack,registration failed"}), 400)
            try:
                emailnotification(req)
            except:
                return make_response(jsonify({"message": "Unable to send email,registration failed"}), 400)
            '''
            
            return DB.Registration.newuser(req,mysql)

    else:

        return make_response(jsonify({"message": "Request body must be JSON"}), 400)

if __name__== "__main__":
    app.run (debug=True)

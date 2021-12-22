from flask import Flask,request,render_template

from flask_mysqldb import MySQL
import smtplib

import slack
import os
from pathlib import Path
from dotenv import load_dotenv




app= Flask(__name__)
#api routes

app.config['MYSQL_HOST']="localhost"
app.config['MYSQL_USER']="root"
app.config['MYSQL_PASSWORD']="Password"
app.config['MYSQL_DB']="usertest"

#mail




mysql = MySQL(app)
@app.route("/email")
def testemail():
        notification_message = ("New User reg. details : User Name:"+username +", Email: " + email + ", First name: " +FirstName+ ", Last Name: " +LastName+ ", Account No: "+accnt_no)
        print(type(notification_message))



@app.route("/user/registration",methods=['GET','POST'])
def members():
    env_path =  Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)
    
    if request.method =='POST':
        username=request.form['username']
        email=request.form['email']
        #pwwd=request.form['pwd']
        FirstName=request.form['First_name']
        LastName=request.form['Last_name']
        accnt_no=request.form['accntno']


        cur=mysql.connection.cursor()
        new_value = cur.execute("SELECT * FROM user WHERE accountno =%s", [accnt_no])
        if new_value> 0 :
            return"user exists already"

        cur.execute("INSERT INTO user(username,firstname,lastname,email,accountno) VALUES (%s,%s,%s,%s,%s)",(username,FirstName,LastName,email,accnt_no))
        mysql.connection.commit()
        cur.close()
        #
        notification_message = ("New User reg. details : User Name:"+username +", Email: " + email + ", First name: " +FirstName+ ", Last Name: " +LastName+ ", Account No: "+accnt_no)
        #email notification

        from_email='dev.tester.env@gmail.com'
        from_email_pwd='password'
        to_email='sampleemail@gmail.com'
        server= smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        server.login(from_email,from_email_pwd)
        server.sendmail(from_email,to_email,notification_message)

        #below is token for slack bot
        SLACK_TOKEN ='xoxb-2866008942450-2882856277889-OwrCBhr9fuqInc6KwwUmFe44'    
        client = slack.WebClient(token=SLACK_TOKEN)
        client.chat_postMessage(channel='#test',text=notification_message)


        
    return render_template('index.html')

if __name__== "__main__":
    app.run (debug=True)

'''\
How to use:
python email.py
requierd config vars:
    DB_URL=<database url>
    TOKEN_ENCRYPT_KEY=key used to encrypt tokens (get from heroku config")
    MAIL_PASSWORD=Password for the schoologycalender mail account
'''

import psycopg2
import os



import schoolopy
from cryptography.fernet import Fernet
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import schedule
import time

MAILSENDER="schoologycalendar@gmail.com"


def sendEmailCourses(crsDict, rec, mailServer):
    bString=""
    bText=""
    for course in crsDict:
        bText=bText+"\n"+course
        bString=bString+"<p>"+course+"</p><ol>"
        for assignment in crsDict[course]:
            bText=bText+"\n\t"+assignment
            bString=bString+"<li style=\"list-style-type:disc;\">"+assignment+"</li>"
        bString=bString+"</ol>"
    
    bod="""<html><head><meta charset="UTF-8"><style>
.page-header {
	background-color: rgb(30,180,210);
	color: rgb(255,255,255);
	text-align: center;
}
	</style>
  </head>
  <body>
    <section class="page-header">
	  <br>
      <h1 class="project-name">Schoology Calendar Notifications</h1>
	  <br>
    </section>

    <section class="course-content">
	  <h2>Assignments</h2>
		%s
	</section>
</body>
</html>""" % bString
    message = MIMEMultipart("alternative")
    message["Subject"] = "Courses for Today"
    message["From"] = MAILSENDER
    message["To"] = rec
    p1=MIMEText(bText,"plain")
    p2=MIMEText(bod,"html")
    message.attach(p1)
    message.attach(p2)
    mailServer.sendmail(MAILSENDER,rec,message.as_string())

def decrypt_message(message):
    f=Fernet(os.environ.get("TOKEN_ENCRYPT_KEY").encode())
    return f.decrypt(message.encode()).decode()

def getUserCourse(crs):
    crs=crs[2:-2]
    crs=crs.replace("'", "")
    crs=crs.split(",")
    crs = [int(i) for i in crs]
    return crs


def sendEmailUser(user, ms):
    access_token=decrypt_message(user[4])
    access_token_secret=decrypt_message(user[5])

    auth = schoolopy.Auth(os.getenv('SCHOOLOGY_KEY'), os.getenv('SCHOOLOGY_SECRET'), domain='https://schoology.harker.org/', access_token=access_token, access_token_secret=access_token_secret, three_legged=True) 
    auth.oauth.token = {'oauth_token': access_token, 'oauth_token_secret': access_token_secret}
    sc=schoolopy.Schoology(auth)
    me=sc.get_me()
    print(me.username)
    crs=getUserCourse(user[3])
    retDict={}
    for course in crs:
        retList=[]
        try:
            sec=sc.get_section(course).section_title
            assignments=sc.get_assignments(section_id=course)
        except Exception as e:
            print(e)
            assignments=[]
        for assignment in assignments:
            try:
                due=assignment.due
                due=datetime.strptime(due, "%Y-%m-%d %H:%M:%S")
                now=datetime.now()#-timedelta(hours=8) #pst
                if (7>(due-now).days>-2):
                    retList.append(assignment.title)
            except Exception:
                pass
        if len(retList)>0:
            retDict[sec]=retList
    try:
        sendEmailCourses(retDict, me.primary_email,ms)
    except Exception as e:
        print(e)


def sendEmailAllUsers():
    try:
        os.system("""DB_URL=$(heroku config:get DATABASE_URL -a harker-schoology-notifications)""")
    except Exception as e:
        print(e)
    DB_URL=os.environ.get("DATABASE_URL")
    print(DB_URL)
    conn=psycopg2.connect(DB_URL)
    cur=conn.cursor()
    cur.execute("SELECT * FROM \"user\";")
    
    #email
    mailServer=smtplib.SMTP_SSL("smtp.googlemail.com", 465)
    mailServer.login(MAILSENDER, os.environ.get("MAIL_PASSWORD"))
    users=cur.fetchall()
    print(users)
    for user in users:
        print(user[4],user[5])
        try:
            sendEmailUser(user, mailServer)
        except Exception as e:
            print(e)
            continue

sendEmailAllUsers()
schedule.every().day.at("08:00").do(sendEmailAllUsers)
#schedule.every().minute.at(":0").do(job)
while True:
    schedule.run_pending()
    time.sleep(1)
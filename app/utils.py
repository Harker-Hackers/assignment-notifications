from app.models import User, getUserCourse
from eMail import eMail
from schoolopyInfo import scAuth, authDict, scAuthVer
from datetime import datetime
from flask import render_template

def sendEmail():
    for user in User.query.all():
        try:
            sAuth=scAuthVer(user.username)
            if sAuth.setSc()==False:
                continue
            sc=sAuth.sc
            me=sc.get_me()
            crs=getUserCourse(user)
            retDict={}
            for course in crs:
                retList=[]
                sec=sc.get_section(course).section_title
                try:
                    assignments=sc.get_assignments(section_id=course)
                except Exception:
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
            mymail=eMail()
            mymail.msg.html=render_template("email.html", person=me, assignments=retDict)
            mymail.msg.subject="Courses for today"
            mymail.recipients=[me.primary_email]
            mymail.send()
        except Exception:
            pass
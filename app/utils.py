from app.models import User, getUserCourse
from eMail import eMail
from schoolopyInfo import scAuth, authDict, scAuthVer
from datetime import datetime

def sendEmail():
    for user in User.query.all():
        sAuth=scAuthVer(user.username)
        if sAuth.setSc()==False:
            continue
        sc=sAuth.sc
        
        crs=getUserCourse(user)
        retList=[]
        for course in crs:
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
        mail=eMail()
        mail.body=str(retList)
        mail.recipients=[sc.get_me().primary_email]
        mail.send()
#basic modules for routes
from flask import Flask, redirect, url_for, send_file, render_template, flash, request, abort, send_from_directory
import schoolopy
from datetime import datetime, timedelta

#app instance + other important instances
from app import app, db

#more schoolopy
from schoolopyInfo import scAuth, authDict
authDict=authDict()

#mail
from eMail import eMail

#sel
from selFunc import getCourses

#models
from app.models import User, getUserCourse

#index
@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')

#login
@app.route('/login')
def login():
    auth, authid=authDict.addTempAuth()
    return redirect(auth.schoolopyUrl+"?aId="+str(authid))

#success
@app.route('/authorized')
def authorized():
    try:
        tok=authDict.verifyAuth(request.args.get("aId"), request.args.get("oauth_token"))
        sAuth=authDict.getAuth(tok)
    except Exception:
        tok=request.args.get("tok")
        sAuth=authDict.getAuth(tok)
    try:
        sc = sAuth.sc
        me=sc.get_me()
    except Exception:
        return render_template("404.html", error="Invalid Token")
    name=me.username
    my_user=User.query.filter_by(username=name)
    try:
        my_user=my_user.first()
        if (my_user==None):
            raise Exception
    except Exception:
        my_user = User(username=name, discId=0,courses="")
        db.session.add(my_user)
        db.session.commit()
    if (request.args.get("man")=="t"):
        return render_template('authorized.html', person=me, tok=tok)
    return render_template('authorized2.html', person=me, tok=tok)

#getting course info
@app.route("/set_courses")
def set_courses():
    sAuth=authDict.getAuth(request.args.get("tok"))
    try:
        sc = sAuth.sc
        name = sc.get_me().username
    except Exception:
        return render_template("404.html", error="Invalid Token")
    k=1
    crs="["
    while True:
        print("i"+str(k))
        try:
            cId=request.args.get("i"+str(k))
            if (cId==None):
                crs=crs[0:-2]
                crs=crs+"]"
                break
            try:
                cId=int(cId)
            except Exception:
                return render_template("404.html", error="Invalid course name")
            crs=crs+"'"+str(cId)+"', "
            k+=1
        except Exception:
            crs=crs[0:-2]
            crs=crs+"]"
            break
    user=User.query.filter_by(username=name).first()
    user.courses=str(crs)
    db.session.commit()
    return redirect(url_for("get_assignments", tok=request.args.get("tok")))

@app.route("/get_courses", methods=["GET", "POST"])
def get_courses():
    sAuth=authDict.getAuth(request.args.get("tok"))
    try:
        sc = sAuth.sc
        name = sc.get_me().username
    except Exception:
        return "Bad tok"
    pw=request.form["pw"]
    try:
        crs=getCourses(name,pw)
        try:
            crs[0]
        except Exception:
            return "Bad pw"
    except Exception:
        return render_template("404.html", error="Server couldn't get info")
    user=User.query.filter_by(username=name).first()
    user.courses=str(crs)
    db.session.commit()
    return redirect(url_for("get_assignments", tok=request.args.get("tok")))

@app.route("/assignments")
def get_assignments():
    sAuth=authDict.getAuth(request.args.get("tok"))
    try:
        sc = sAuth.sc
        name = sc.get_me().username
    except Exception:
        return "bad"
    my_user=User.query.filter_by(username=name).first()
    crs=getUserCourse(my_user)
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
                print((due-now).days)
                if (7>(due-now).days>-2):
                    retList.append(assignment.title)
            except Exception:
                pass
    return str(retList)
#sending an email
'''
@app.route('/email')
def sendEmail():
    eml=eMail()
    eml.recipients=["25aarushv@students.harker.org"]
    eml.head="Hello"
    eml.body="HELLOS"
    eml.send()
    return "success"
'''
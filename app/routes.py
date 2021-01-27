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
    return redirect(url_for("hub",tok=tok))

#main hub
@app.route("/hub")
def hub():
    tok=request.args.get("tok")
    sAuth=authDict.getAuth(tok)
    try:
        sc = sAuth.sc
        me = sc.get_me()
    except Exception:
        return render_template("404.html", error="Invalid Token")
    my_user=User.query.filter_by(username=me.username).first()
    try:
        crs=getUserCourse(my_user)
        crsNames=[]
        for i in crs:
            try:
                sec=sc.get_section(i).section_title
                crsNames.append(sec)
            except Exception:
                continue
    except Exception:
        crsNames=[]
    return render_template("hub.html", person=me, courses=crsNames, tok=tok)

#getting course
@app.route("/get_courses")
def get_courses():
    tok=request.args.get("tok")
    sAuth=authDict.getAuth(tok)
    try:
        sc = sAuth.sc
        me = sc.get_me()
    except Exception:
        return render_template("404.html", error="Invalid Token")
    return render_template("authorized2.html", person=me, tok=tok)
    
#setting course
@app.route("/set_courses")
def set_courses():
    tok=request.args.get("tok")
    sAuth=authDict.getAuth(tok)
    try:
        sc = sAuth.sc
        me = sc.get_me()
        my_user = User.query.filter_by(username=me.username).first()
    except Exception:
        return render_template("404.html", error="Invalid Token")
    try:
        courses=getUserCourse(my_user)
        courseNames=request.args.get("crs")
    except Exception:
        courses=""
        courseNames=""
    return render_template("authorized.html", person=me, tok=tok, courses=str(courses), courseNames=str(courseNames))

#getting course info
@app.route("/sccallback")
def set_courses_callback():
    sAuth=authDict.getAuth(request.args.get("tok"))
    try:
        sc = sAuth.sc
        name = sc.get_me().username
    except Exception:
        return render_template("404.html", error="Invalid Token")
    k=1
    crs="["
    while True:
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
    return redirect(url_for("hub", tok=request.args.get("tok")))

@app.route("/gccallback", methods=["GET", "POST"])
def get_courses_callback():
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
    return redirect(url_for("hub", tok=request.args.get("tok")))

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

@app.errorhandler(500)
def server_error(err):
    return render_template('500.html')

@app.errorhandler(404)
def not_found_error(err):
    return render_template('404.html')
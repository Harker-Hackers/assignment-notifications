#basic modules for routes
from flask import Flask, redirect, url_for, send_file, render_template, flash, request, abort, send_from_directory
import schoolopy

#app instance + other important instances
from app import app, db

#more schoolopy
from schoolopyInfo import schoolopyAuth, schoolopyUrl

#mail
from eMail import eMail

#sel
from selFunc import getCourses

#models
from app.models import User, getUserCourse

#index
@app.route('/', methods=["GET", "POST"])
def index():
    return "add me to the hangout again i didn't get it"

#login
@app.route('/login')
def login():
    return redirect(schoolopyUrl)

#success
@app.route('/authorized')
def authorized():
    if not schoolopyAuth.authorize():
        return redirect(url_for('login'))
    sc = schoolopy.Schoology(schoolopyAuth)
    me=sc.get_me()
    name = sc.get_me().username
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
        return render_template('authorized.html', person=me)
    return render_template('authorized2.html', person=me)

#getting course info
@app.route("/set_courses")
def set_courses():
    if not schoolopyAuth.authorize():
        return redirect(url_for('login'))
    sc = schoolopy.Schoology(schoolopyAuth)
    name = sc.get_me().username
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
                return redirect(url_for("authorized"))
            crs=crs+"'"+str(cId)+"', "
            k+=1
        except Exception:
            crs=crs[0:-2]
            crs=crs+"]"
            break
    user=User.query.filter_by(username=name).first()
    user.courses=str(crs)
    db.session.commit()
    return crs

@app.route("/get_courses", methods=["GET", "POST"])
def get_courses():
    if not schoolopyAuth.authorize():
        return redirect(url_for('login'))
    sc = schoolopy.Schoology(schoolopyAuth)
    name = sc.get_me().username
    pw=request.form["pw"]
    try:
        crs=getCourses(name,pw)
        crs[0]
    except Exception:
        return redirect(url_for('get_courses'))
    user=User.query.filter_by(username=name).first()
    user.courses=str(crs)
    db.session.commit()
    return crs
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
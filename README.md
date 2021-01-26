# harker-calendar-notifications
Be notified on discord of upcoming assignments from Schoology. Made using @schoology's REST API, the @discord API, and selenium.


--- How to use migrations ---
1. Make change to models.py
2. Locally run "flask db migrate"
  This will make a migration file with the code required to update the db
3. flask db upgrade - upgrades the local db
4. git commit
5. heroku run flask db upgrade - upgrades heroku's database

--- How to use the selenium addition ---
1. from selFunc import getCoruses
2. getCourses("<username>", "<password>")
3. This will return a list with the course ids

--- How to use the new db ---
Comms:
'''Make a user'''
new_user = User(username=<String username>, discId=<int id>, courses="")
db.session.add(new_user) #adds the user to the session
db.session.commit() #makes changes final, can't rollback due to free db
'''Delete a user'''
del_user = User.query.get(1) #gets user with id 1
#del_user should be the user you want to delete
db.session.delete(del_user)
db.session.commit()
'''Get all users'''
User.query.all()
'''Get user by id'''
User.query.get(<int id>)
'''Get user by username'''
my_user=User.query.filter_by(username='Name').first()
'''Get user courses'''
my_user.courses
'''Update courses'''
my_user.courses='NEW COURSES'

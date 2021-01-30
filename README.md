<p align="center"><img src="https://p11cdn4static.sharpschool.com/UserFiles/Servers/Server_141067/Image/sgy%20logo%20resized.png" width="80" legnth="80"></p>
<h1 align="center">Harker Calendar Notifications</h1>
  <p align="center">Be notified on discord of upcoming assignments from Schoology every morning.<br>
  <sub>By <a href="https://github.com/goombamaui">Aarush Vailaya</a> and <a href="http://github.com/gadhagod">Aarav Borthakur</a>.</sub></p>
  
## Usage
Go to [http://harker-schoology-notifications.herokuapp.com/](http://harker-schoology-notifications.herokuapp.com/) and click "login". Aprove access. That's it! Now you will recieve an email every morning. You can explore the hub too.
  
## Local Hosting
  
**How to use migrations**
1. Install requirements with `pip3 install -r requirements.txt`.
1. Make change to models.py.
2. Locally run `flask db migrate`.
  This will make a migration file with the code required to update the database.
3. `flask db upgrade` - upgrades the local db
4. `git commit`
5. `heroku run flask db upgrade` - upgrades heroku's database

**How to use the selenium addition**
1. 
```python
from selFunc import getCourses
getCourses("<username>", "<password>")
```
2. This will return a list with the course ids

**How to use the new database**
Comms:
```python
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
db.session.commit()
```
**How to send email to all users**
1. Go to /email_ver
2. enter pw
3. Email sent

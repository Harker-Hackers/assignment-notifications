import subprocess

rc=subprocess.run(["heroku config:get DATABASE_URL"])

print(rc.return_code)
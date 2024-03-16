#!/usr/bin/env python3
from flask import Flask

app = Flask(__name__)

@app.route("/")
@app.route("/webcsv")
def hello(subpath=None):
  return "<pre>Hello, world! This is webcsv running <b>Flask</b>!</pre>"


# Create & start daemon with app:
#   gunicorn app:app -n flaskapp -w 2 -u ray -g staff -b :8001 -D

# Stop app process (daemon):
#  kill -9 <ppid>

# Check running (daemon) from processes on Mac OS:
#  ps aux | grep '[f]laskapp' --color=always | sed 's/Library.*MacOS/.../g'

# Check all gunicorn apps/processes:
#  ps aux | grep '[g]unicorn' --color=always | sed 's/Library.*MacOS/.../g'
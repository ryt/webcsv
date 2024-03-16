#!/usr/bin/env python3

# This app uses Flask & Runapp (ryt/runapp).

# Create & start gunicorn (daemon/process) with app:
# $ cd webcsv
# $ ./runapp start

# Stop app process:
# $ ./runapp stop

# Check running app process:
# $ ./runapp list

# Restart app process:
# $ ./runapp restart


from flask import Flask, request



app = Flask(__name__)

@app.route("/")
@app.route("/webcsv")

def hello(subpath=None):

  nl = '\n'
  html = []

  getf = request.args.get('f')

  html += ['<h3>webcsv</h3>']
  html += [f'<p>current value of <b>f</b> is: <u>{getf}</u>']

  return nl.join(html)


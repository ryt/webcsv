#!/usr/bin/env python3

# This app uses Flask & Runapp/Gunicorn (ryt/runapp) for Deployment.

# Create & start a deployment, gunicorn (daemon/process), with app:
# $ cd webcsv
# $ ./runapp start

# Stop deployment/app process:
# $ ./runapp stop

# Check running deployment/app process:
# $ ./runapp list

# Restart deployment/app process:
# $ ./runapp restart

# If not running after restart, check & re-deploy:
# $ ./runapp list
# $ ./runapp start


from flask import Flask
from flask import request
from flask import render_template



app = Flask(__name__)

@app.route('/')
@app.route('/webcsv')

def index(subpath=None):

  nl = '\n'
  getf = request.args.get('f')

  return render_template('template.html', getf=getf)


if __name__ == '__main__':
    app.run(debug=True)


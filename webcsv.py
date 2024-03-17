#!/usr/bin/env python3

# This app uses Flask & Gunicorn with ryt/runapp for deployment.

# Create & start a deployment, gunicorn (daemon/process), with runapp:
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

import os
import csv

from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

def html_return_error(text):
  return f'<div class="error">{text}</div>'

def html_render_csv(path):

  render = ''

  try:

    with open(path, 'r') as file:
      content = file.read()
      html_table = '<table class="csv-table">\n'

      csv_reader = csv.reader(content.splitlines())
      headers = next(csv_reader)

      html_table += '<tr>'
      for header in headers:
        html_table += f'<th>{header}</th>'
      html_table += '</tr>\n'

      for row in csv_reader:
        html_table += '<tr>'
        for cell in row:
          html_table += f'<td>{cell}</td>'
        html_table += '</tr>\n'
      
      html_table += '</table>'

      render = html_table

  except FileNotFoundError:
    render = html_return_error(f"The file '{path}' does not exist.")

  except IOError:
    render = html_return_error(f"Error reading the file '{path}'.")

  return render


@app.route('/')
@app.route('/webcsv')

def index(subpath=None):

  getf = request.args.get('f') or ''
  view = {}
  newfs = []

  if os.path.isdir(getf):
    files = sorted(os.listdir(getf))
    parpt = getf.rstrip('/')
    if files:
      for f in files:
        if os.path.isdir(f'{parpt}/{f}'):
          newfs.append((f'{f}/', f'{parpt}/{f}/'))
        else:
          newfs.append((f, f'{parpt}/{f}'))
  else:
    view['noncsv'] = True

  if getf.endswith('.csv'):
    view['csvshow'] = html_render_csv(getf)
    view['noncsv']  = False

  address = []
  addrbuild = ''
  if getf:
    for path in getf.strip('/').split('/'):
      addrbuild += f'/{path}'
      address.append((f'{path}', f'{addrbuild}', '/'))

  view['getf']    = getf
  view['newfs']   = newfs
  view['address'] = address


  return render_template('template.html', view=view)


if __name__ == '__main__':
    app.run(debug=True)


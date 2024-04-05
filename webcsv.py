#!/usr/bin/env python3

# This app uses Flask & Gunicorn with ryt/runapp for deployment.

v = '0.0.2'

"""
Copyright (C) 2024 Ray Mentose.
Latest version of the project on Github at: https://github.com/ryt/webcsv
"""

import os
import csv
import html
import itertools

from flask import Flask
from flask import request
from urllib.parse import quote
from flask import render_template
from configparser import ConfigParser

app = Flask(__name__)

limitpath = ''

def html_return_error(text):
  return f'<div class="error">{text}</div>'

def html_render_csv(path):

  render   = ''
  path_mod = remove_limitpath(path)

  try:

    with open(path, 'r') as file:
      content = file.read()
      html_table = '<table class="csv-table">\n'

      csv_reader = csv.reader(content.splitlines())
      headers = next(csv_reader)

      html_table += '<tr>'
      for header in headers:
        header = html.escape(header)
        html_table += f'<th>{header}</th>'
      html_table += '</tr>\n'

      for row in csv_reader:
        html_table += '<tr>'
        for cell in row:
          cell = html.escape(cell)
          html_table += f'<td>{cell}</td>'
        html_table += '</tr>\n'
      
      html_table += '</table>'

      render = html_table

  except FileNotFoundError:
    render = html_return_error(f"The file '{path_mod}' does not exist.")

  except IOError:
    render = html_return_error(f"Error reading the file '{path_mod}'.")

  return render


def plain_render_file(path):

  render   = ''
  path_mod = remove_limitpath(path)

  try:
    with open(path, 'r') as file:
      try:
        render = file.read()
      except:
        render = f"The file '{path_mod}' is not in text format."

  except FileNotFoundError:
    render = f"The file '{path_mod}' does not exist."

  except IOError:
    render = f"Error reading the file '{path_mod}'."

  return render

def remove_from_start(sub, string):
  """Remove sub from beginning of string if string starts with sub"""
  if string.startswith(sub):
    return string[len(sub):].lstrip()
  else:
    return string

def remove_limitpath(path):
  """Remove limitpath from beginning of path if limitpath has value"""
  global limitpath
  return remove_from_start(limitpath, path) if limitpath else path

def add_limitpath(path):
  """Add limitpath to beginning of path if limitpath has value"""
  global limitpath
  return f'{limitpath}{path}' if limitpath else path

def sanitize_path(path):
  """Sanitize path for urls: 1. apply limitpath mods, 2. escape &'s and spaces"""
  return quote(remove_limitpath(path), safe='/')

sp = sanitize_path


@app.route('/')
@app.route('/webcsv')

def index(subpath=None):

  # if limitpath is set, the internal path will be limited to that path as the absolute parent
  global limitpath

  # -- start: parse runapp.conf (if it exists) and modify limitpath (if it exists)
  conf = 'runapp.conf'
  if os.path.exists(conf):
    with open(conf) as cf:
      config = ConfigParser()
      config.read_file(itertools.chain(['[global]'], cf), source=conf)
      try:
        limitpath = config.get('global', 'limitpath').rstrip('/') + '/'
      except:
        limitpath = ''
  # -- end: parse runapp config

  # limitpath = '/usr/local/share/' # for testing

  getf      = request.args.get('f') or ''
  getview   = request.args.get('view') or ''

  getf_html   = remove_limitpath(getf) # limitpath mods applied
  getf        = add_limitpath(getf)

  view = {}
  listfs = []

  if os.path.isdir(getf):
    files = sorted(os.listdir(getf))
    parpt = getf.rstrip('/')
    if files:
      for f in files:
        if os.path.isdir(f'{parpt}/{f}'):
          listfs.append({ 
            'name' : f'{f}/', 
            'path' : sp(f'{parpt}/{f}/')
          })
        else:
          listfs.append({ 
            'name' : f, 
            'path' : sp(f'{parpt}/{f}')
          })
  else:
    view['noncsv'] = True
    view['noncsv_plain'] = plain_render_file(getf) if getview == 'plain' else ''

  if getf.endswith('.csv'):
    view['csvshow'] = html_render_csv(getf)
    view['noncsv']  = False

  address = []
  addrbuild = ''
  if getf_html: 
    for path in getf_html.strip('/').split('/'):
      addrbuild += f'/{path}'
      address.append({ 
        'name' : f'{path}', 
        'path' : sp(f'{addrbuild}'),
        'separator' : '/'
      })

  view['listfs']          = listfs
  view['address']         = address
  view['getf_html']       = getf_html
  view['getf_html_sp']    = sp(getf_html)
  view['getview_query']   = f'&view={getview}' if getview else ''
  view['show_header']     = True

  hide = request.args.get('hide')

  if hide and hide == 'true':
    view['show_header'] = False

  return render_template('template.html', view=view)


if __name__ == '__main__':
    app.run(debug=True)


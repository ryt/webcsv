#!/usr/bin/env python3

# This app uses Flask & Gunicorn with ryt/runapp for deployment.

v = '0.0.3'

"""
Copyright (C) 2024 Ray Mentose.
Latest version of the project on Github at: https://github.com/ryt/webcsv
"""

import os
import csv
import html
import config
import itertools

from flask import Flask
from flask import request
from urllib.parse import quote
from flask import render_template

app = Flask(__name__)

# -- start: parse config parameters from config.py and set values

# default config values

limitpath = ''
app_path  = '/webcsv'
parse_markdown  = False
parse_html      = False

# read & modify config values

if 'limitpath' in config.config:
  limitpath = config.config['limitpath'].rstrip('/') + '/'

if 'app_path' in config.config:
  app_path = config.config['app_path']

if 'parse_markdown' in config.config:
  parse_markdown = config.config['parse_markdown']

if 'parse_html' in config.config:
  parse_html = config.config['parse_html']

# -- end: parse config parameters

# markdown options
if parse_markdown == True:
  from marko.ext.gfm import gfm


def get_query(param):
  """Get query string param (if exists & has value) or empty string"""
  try:
    return request.args.get(param) if request.args.get(param) else ''
  except:
    return ''

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

def parse_filter(qfilter):
  """Parse a filter (query) string and convert it into dictionary with keys, values, & attributes"""
  filter_dicts = []
  filter_instances = qfilter.split(',')
  for f in filter_instances:
    filter_parts = f.split(':')
    filter_key = filter_parts[0]
    filter_val = filter_parts[1]
    filter_col_num = int(''.join(filter(str.isdigit, filter_key)))
    filter_dicts.append({
      'key'     : filter_key,
      'col_num' : filter_col_num,
      'val'     : filter_val
    })

  return filter_dicts

def filter_compare(csv_value, search_value):
  """Compares csv_value & search_value and determines if the filters match or not"""

  # quoted strings == exact match

  if (search_value.startswith('"') and search_value.endswith('"')) or (search_value.startswith("'") and search_value.endswith("'")):
    if search_value.strip('\'"') == csv_value:
      return True
    else:
      return False

  # non-quoted strings = search

  elif search_value in csv_value:
    return True

  return False

def html_return_error(text):
  return f'<div class="error">{text}</div>'

def html_render_csv(path):

  render   = ''
  path_mod = remove_limitpath(path)

  try:

    with open(path, 'r') as file:

      getfilter = get_query('filter')
      html_table = ''

      content = file.read()

      if getfilter:
        filter_insts = parse_filter(getfilter)
        filter_ihtml = [f"<b>{f['key']}</b> = <b>{f['val']}</b>" for f in filter_insts]
        html_table = f'<div class="top-filter">Applying filter: {", ".join(filter_ihtml)}. Filtered rows: ##__filtered_rows__##.</div>'


      html_table += '<table class="csv-table">\n'
      # added {skiinitialspace=True} to fix issue with commas inside quoted cells
      csv_reader = csv.reader(content.splitlines(), skipinitialspace=True)
      headers = next(csv_reader)

      html_table += '<tr>'
      for header in headers:
        header = html.escape(header)
        html_table += f'<th>{header}</th>'
      html_table += '</tr>\n'

      filtered_rows = 0

      for row in csv_reader:
        display_row = True

        if getfilter:
          display_row = False
          fi = filter_insts
          table_row = '<tr>'

          if len(fi) > 1: # multiple filters (AND search)
            found_count = 0

            for fx in fi:
              if 0 <= fx['col_num']-1 < len(row) and filter_compare(row[fx['col_num']-1], fx['val']):
                found_count += 1 # add 1 for each found filter

            if found_count == len(fi):
              display_row = True

          else: # single filter
            if 0 <= fi[0]['col_num']-1 < len(row) and filter_compare(row[fi[0]['col_num']-1], fi[0]['val']):
              display_row = True


          for cell in row:
            cell = html.escape(cell)
            table_row += f'<td>{cell}</td>'

          table_row += '</tr>\n'

        else:
          table_row = '<tr>'
          for cell in row:
            cell = html.escape(cell)
            table_row += f'<td>{cell}</td>'
          table_row += '</tr>\n'

        if display_row:
          filtered_rows += 1
          html_table += table_row
      

      html_table += '</table>'

      render = html_table.replace('##__filtered_rows__##', str(filtered_rows))

  except FileNotFoundError:
    render = html_return_error(f"The file '{path_mod}' does not exist.")

  except:
    render = html_return_error(f"The file '{path_mod}' could not be parsed.")

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


def noncsv_render_file(path, ftype):

  render   = ''
  path_mod = remove_limitpath(path)

  try:
    with open(path, 'r') as file:
      try:
        if ftype == 'markdown':
          render = f'<article class="markdown-body">{gfm(file.read())}</article>'
        elif ftype == 'html':
          render = file.read()
        else:
          render = f"The file '{path_mod}' is not in supported format."
      except:
        render = f"The file '{path_mod}' is not in a supported format."

  except FileNotFoundError:
    render = f"The file '{path_mod}' does not exist."

  except IOError:
    render = f"Error reading the file '{path_mod}'."

  return render


@app.route(app_path, methods=['GET'])

def index(subpath=None):

  # if limitpath is set in config, the directory listing view for the client/browser will be limited to that path as the absolute parent
  # if app_path is set in config, that path will be used to route index page of the app

  global limitpath, app_path

  # limitpath = '/usr/local/share/' # for testing

  getf        = get_query('f')
  getview     = get_query('view')
  getfilter   = get_query('filter')
  getf_html   = remove_limitpath(getf)  # limitpath mods for client/browser side view
  getf        = add_limitpath(getf)     # limitpath mods for internal processing

  view   = { 
    'app_path'  : app_path, 
    'getfilter' : getfilter 
  }
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
    # additional non-csv rendering options
    # markdown
    if parse_markdown == True and getf.endswith('.md'):
      view['noncsv'] = True
      view['noncsv_markdown'] = noncsv_render_file(getf, 'markdown')
      with open('assets/github-markdown.css', 'r') as github_markdown:
        view['markdown_css'] = github_markdown.read()
    # html
    elif parse_html == True and (getf.endswith('.htm') or getf.endswith('.html')):
      view['noncsv'] = True
      view['noncsv_html'] = noncsv_render_file(getf, 'html')
    # plain
    else:
      view['noncsv'] = True
      view['noncsv_plain'] = plain_render_file(getf) if getview == 'plain' else ''



  if getf.endswith('.csv'):
    view['csvshow'] = html_render_csv(getf)
    view['noncsv']  = False

  address   = []
  addrbuild = ''
  if getf_html: 
    for path in getf_html.strip('/').split('/'):
      addrbuild += f'/{path}'
      address.append({ 
        'name'      : f'{path}', 
        'path'      : sp(f'{addrbuild}'),
        'separator' : '/'
      })

  view['listfs']          = listfs
  view['address']         = address
  view['getf_html']       = getf_html
  view['getf_html_sp']    = sp(getf_html)
  view['getview_query']   = f'&view={getview}' if getview else ''
  view['getfilter_query'] = f'&filter={getfilter}' if getfilter else ''
  view['show_header']     = False if get_query('hide') == 'true' else True


  return render_template('template.html', view=view)


if __name__ == '__main__':
    app.run(debug=True)


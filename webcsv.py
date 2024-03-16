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


from flask import Flask, request



app = Flask(__name__)

@app.route("/")
@app.route("/webcsv")

def index(subpath=None):

  nl = '\n'
  s  = ' '

  html = [
    '<!DOCTYPE html>',
    '<html>',
    f'{s*2}<head>',
    f'{s*4}<meta charset="UTF-8">',
    f'{s*4}<title>webcsv: Simple CSV Web Viewer</title>',
    f'{s*4}<style>',
    f'{s*6}' + f'{nl}{s*6}'.join((
        'body { margin:0; font:16px sans-serif; }',
        'h2 { margin:0;padding:8px 16px;background:#ddd;border-bottom:1px solid #ccc; }',
        'p { margin:0;padding:8px 16px; }',
      )),
    f'{s*4}</style>',
    f'{s*2}</head>',
    f'{s*2}<body>',
  ]

  getf = request.args.get('f')

  html += [f'{s*4}<h2>webcsv</h2>']
  html += [f'{s*4}<p>current value of <b>f</b> is: <u>{getf}</u>']

  html += [f'{s*2}</body>']
  html += ['</html>']

  return nl.join(html)


if __name__ == '__main__':
    app.run(debug=True)


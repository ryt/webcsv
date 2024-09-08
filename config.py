#!/usr/bin/env python3

config = {

  # Set 'limitpath' to a custom value to change the default absolute directory for the directory listing view 
  # of the client/browser when the web app is loaded. By default, the directory is "/", the root directory.

  #'limitpath' : '/home/user/project/',

  # Set 'app_path' to a custom value to change the default path that will be used to route the index page of the app.
  # For example, if the value is "/webcsv", the default url of the web app will be something like 
  # "https://localhost:8002/webcsv", rather than "https://localhost:8002/".

  'app_path'  : '/webcsv',

  # Set 'parse_html' to True to enable webcsv to parse & render html files. Please note that scripts and styles that are
  # included within the html code will be rendered and processed by the browser as well. Make sure the html files are
  # safe to be processed if you enable the 'parse_html' option.

  'parse_html'  : False,

  # Set 'parse_markdown' to True to enable webcsv to parse & render markdown files with a default Github flavored style.
  # If enabled, the app will use the marko library: https://marko-py.readthedocs.io/en/latest/ to parse '.md' files.

  'parse_markdown'  : True,

  # Set 'parse_rst' to True to enable webcsv to parse & render rst (reStructuredText) files with a default Github flavored style.
  # If enabled, the app will use the docutils library: https://docutils.sourceforge.io/rst.html to parse '.rst' files.

  'parse_rst'  : True,

}

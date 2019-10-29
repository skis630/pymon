import os
from sys import argv
from bottle import run

from backend.handlers import app
from backend.static_handlers import staticHandler
from backend.page_handlers import pageHandler


app.merge(staticHandler)
app.merge(pageHandler)
run(app, host='0.0.0.0', port=argv[1])
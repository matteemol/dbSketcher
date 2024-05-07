# Importing required functions
from flask import Flask, flash, render_template, request, abort, send_from_directory, send_file

import os

basedir = os.path.abspath(os.path.dirname(__file__))

# Flask constructor
app = Flask(__name__)

# Index page
@app.route('/')
def index():
#	linktojarfile = os.path.join(basedir, 'plantuml-core.jar')
	return render_template('index.html')

@app.route("/tryme/", methods=['POST'])
def try_me():
    return render_template('ok.html')

# Main Driver Function
if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
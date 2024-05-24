# Importing required functions
from flask import Flask, flash, render_template, request, abort, send_from_directory, send_file

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

basedir = os.path.abspath(os.path.dirname(__file__))

from dbsketcher import run
from dbsketcher import formatStrings

# Flask constructor
app = Flask(__name__)

# Index page
@app.route('/')
def index():
#	linktojarfile = os.path.join(basedir, 'plantuml-core.jar')

# Copiar aca las indicaciones de como ejecutar el programa segun el input del textarea
# en lugar de sys.argv llamar las funciones desde aca

	return render_template('index.html')

@app.route("/tryme/", methods=['POST'])
def try_me():
    return render_template('ok.html')


@app.route('/sketch', methods=['POST'])
def sketch():
	print("request received")

	if request.is_json:
		data = request.get_json()
		print(data)
	else:
		print("Request is not JSON")
		
	print(data['csv'])
#	csv = request.form['csv']
	output, umlOutput = run.runHTML(data['csv']);
	print('\n-+-+-+- Output -+-+-+-\n')
	print(umlOutput)
#	return umlOutput, 200, {'Content-Type': 'text/plain'}

	return {
		"umlOutput": umlOutput
	}

#	text = request
#	response = text
#	return response, 200, {'Content-Type': 'text/plain'}


# Main Driver Function
if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
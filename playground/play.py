# Importing required functions
from flask import Flask, flash, render_template, request, abort, send_from_directory, send_file, jsonify

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
	return render_template('index.html')

# Receive a JSON object with the structure required by the main program
# (plain text of the CSV file), and run the program with this text.
@app.route('/sketch', methods=['POST'])
def sketch():
	print("request received")

	if request.is_json:
		data = request.get_json()
		print(data)
	else:
		print("Request is not JSON")

# Here's the key. runHTML runs the program directly with the text
# instead of requiring the CSV file/route in the command line		
	output, umlOutput = run.runHTML(data['csv'])
	print('\n-+-+-+- Output -+-+-+-\n')
	print(output)
	returnOutput = { "uml": umlOutput}

	return jsonify(returnOutput), 200, {'Content-Type': 'application/json'}


# Main Driver Function
if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
# Importing required functions
from flask import Flask, flash, render_template, request, abort, send_from_directory, send_file

# Flask constructor
app = Flask(__name__)

# Index page
@app.route('/')
def index():
	return render_template('index.html')

# Main Driver Function
if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
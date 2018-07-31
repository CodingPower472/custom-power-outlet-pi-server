
from flask import Flask, render_template, request, redirect
#from gpiozero import LED
import os


global status
global statusval
global buttonval
buttonval = "Turn off"
status = 1
app = Flask(__name__)

dir = os.getcwd()

@app.route('/', methods=['GET', 'POST'])
def main():
	global status, statusval, buttonval
	if status == 1:
		statusval = "Status: On"

	else: statusval = "Status: off"
	return render_template('index.html', name = statusval, tname = buttonval)


@app.route('/handle_data', methods=['POST'])
def handle_data():
	global status, statusval, buttonval
	if status == 1:
		#turn gpio pin on
		statusval = "Status: Off"
		status = 0
		buttonval = "Turn on"
		return redirect("/", code=302)

	if status == 0:
		#turn gpio pin off
		statusval = "Status: On"
		status = 1
		buttonval = "Turn off"
		return redirect("/", code=302)

if __name__  == "__main__":
	app.run(debug=True)

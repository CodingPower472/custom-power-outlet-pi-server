
from flask import Flask, render_template, request, redirect
#from gpiozero import LED
import os

global isPowered

isPowered = True

app = Flask(__name__)

dir = os.getcwd()

@app.route('/', methods=['GET', 'POST'])
def main():
	return render_template('index.html', isPowered = isPowered)


@app.route('/handle_data', methods=['POST'])
def handle_data():

	global isPowered
	isPowered = not isPowered

	if isPowered:
		print("Turning device on")
		# turn gpio pin off, turning device on
	else:
		print("Turning device off")
		# turn gpio pin on, turning device off
		
	return redirect("/", code = 302)
	

if __name__  == "__main__":
	app.run(debug=True)

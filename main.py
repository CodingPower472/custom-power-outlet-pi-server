
from flask import Flask, render_template, request, redirect
from gpiozero import OutputDevice
import os

RELAY_PIN = 8 # set this to relay pin

global isPowered
isPowered = True

app = Flask(__name__)
relay = OutputDevice(RELAY_PIN, active_high = False, initial_value = False)

# set relay initially off, so device is initially on
relay.off()

dir = os.getcwd()

@app.route('/', methods=['GET', 'POST'])
def main():
	return render_template('index.html', isPowered = isPowered)


@app.route('/handle_data', methods=['POST'])
def handle_data():

	global isPowered
	isPowered = not isPowered

	print("Toggling power to device")
	relay.toggle()
		
	return redirect("/", code = 302)
	

if __name__  == "__main__":
	app.run(debug=True)

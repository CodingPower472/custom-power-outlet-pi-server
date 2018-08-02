
from flask import Flask, render_template, redirect
from gpiozero import OutputDevice
import os
import argparse
from pyhap.accessory import Accessory
from pyhap.const import CATEGORY_LIGHTBULB
from pyhap.accessory_driver import AccessoryDriver
import signal

# argv = sys.argv

RELAY_PIN = 8 # default relay pin

"""
if argv.count > 2 and (argv[1] == '--pin' or argv[1] == '-p'):
	try:
		RELAY_PIN = int(argv[2])
	except ValueError:
		print('Warning: Can\'t parse pin as an integer, defaulting to %i' % RELAY_PIN)
"""

global isPowered
isPowered = True

app = Flask(__name__)
relay = OutputDevice(RELAY_PIN, active_high = False, initial_value = False)

# set relay initially off, so device is initially on
relay.off()

class HomekitDevice(Accessory):

	category = CATEGORY_LIGHTBULB

	@classmethod
	def _gpio_setup(_cls, pin):
		relay = OutputDevice(RELAY_PIN, active_high = False, initial_value = False)
		relay.off()
		print("Setting up GPIO")

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		print("Initting")

		serv_light = self.add_preload_service('Lightbulb')
		self.char_on = serv_light.configure_char('On', setter_callback = self.set_bulb)

		self.pin = RELAY_PIN
		self._gpio_setup(self.pin)

	def __setstate__(self, state):
		print("Setting state")
		self.__dict__.update(state)
		self._gpio_setup(self.pin)

	def set_bulb(self, value):
		print("Setting bulb state to %s" % value)
		if value:
			relay.off()
		else:
			relay.on()

	def stop(self):
		super().stop()

driver = AccessoryDriver(port = 51826)
driver.add_accessory(accessory = HomekitDevice(driver, 'Light 1'))
signal.signal(signal.SIGTERM, driver.signal_handler)

driver.start()

dir = os.getcwd()

@app.route('/', methods=['GET', 'POST'])
def main():
	return render_template('index.html', isPowered = isPowered)


@app.route('/handle_data', methods=['POST'])
def handle_data():

	global isPowered
	isPowered = not isPowered

	print('Toggling power to device')
	relay.toggle()
		
	return redirect("/", code = 302)
	

if __name__  == '__main__':
	app.run(debug=True)

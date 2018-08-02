
from flask import Flask, render_template, redirect
import os
import argparse
from pyhap.accessory import Accessory
from pyhap.const import CATEGORY_LIGHTBULB
from pyhap.accessory_driver import AccessoryDriver
import signal

# argv = sys.argv

RELAY_PIN = 8 # default relay pin

global isPowered
isPowered = True

app = Flask(__name__)

class HomekitDevice(Accessory):

	category = CATEGORY_LIGHTBULB

	@classmethod
	def _gpio_setup(_cls, pin):
		print("Setting up GPIO")

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		print("Initting")

		serv_light = self.add_preload_service('Lightbulb')
		self.char_on = serv_light.configure_char('On', getter_callback = self.get_bulb, setter_callback = self.set_bulb)

		self.pin = RELAY_PIN
		self._gpio_setup(self.pin)

	def __setstate__(self, state):
		print("Setting state")
		self.__dict__.update(state)
		self._gpio_setup(self.pin)

	def get_bulb(arg):
		return isPowered

	def set_bulb(self, value):
		print("Setting bulb state to %s" % value)
		global isPowered
		isPowered = not isPowered

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
		
	return redirect("/", code = 302)
	

if __name__  == '__main__':
	app.run(debug=True)

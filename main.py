
from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
	dir = os.getcwd()
	return send_from_directory(dir, "index.html")

#-*- coding:utf-8 -*-

#author: cheng

from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/', methods = ['GET'])
def index():
	return render_template('index.html')


#@app.route('/code/complete/', methods=['POST'])
def code_complete():
	pass


if __name__ == '__main__':
	app.debug=True
	app.run()
	
#-*- coding:utf-8 -*-

#author: cheng

from flask import Flask, request, jsonify
from flask import render_template

app = Flask(__name__)

from docker_util.client import get_client
from docker_util.util import exec_code

client = get_client()


@app.route('/', methods = ['GET'])
def index():
	return render_template('index.html')


#@app.route('/code/complete/', methods=['POST'])
def code_complete():
	pass

@app.route('/code/submit/', methods=['POST'])
def code_submit():
	if request.method == 'POST':
		code = request.form['code']

		#提交代码，保存代码并运行
		#提交后生成一个submission记录
		#保存代码文件，调用执行环境运行
		exec_code(code=None, account=None, problem_id=None)

		return jsonify({'status': 'ok'})


if __name__ == '__main__':
	app.debug=True
	app.run()
	
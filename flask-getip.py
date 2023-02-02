from flask import Flask,request
import sys

userlist = []

jumptext='跳转失败，您可能开启了代理或者出现了未知错误'

app = Flask(__name__)

@app.route('/get/')
def adminget():
	return str(userlist)

@app.route('/clear/')
def clear():
	global userlist
	userlist=[]
	return '404 not found'

@app.route('/changetext/')
def changetext():
	global jumptext
	jumptext=request.args.get('text')
	return '修改成功！'

@app.route('/jump/')
def jumpa():
	id = request.args.get('jumpid')
	ip = request.remote_addr
	userlist.append({'id':id,'ip':ip})
	return jumptext

if __name__ == '__main__':

	app.run(debug=True,port=int(sys.argv[1]))
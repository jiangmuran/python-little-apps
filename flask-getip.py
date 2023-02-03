from flask import Flask,request
import sys,time,sqlite3


def _initsqlite():
	conn = sqlite3.connect('./flask-getip/ip.db')
	cur = conn.cursor()
	
	cmd = r'''CREATE TABLE ip
(
id TEXT,
ip TEXT,
unixtime NUMBER,
);'''
	print(cmd)




_initsqlite()



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
	userlist.append({"id":id,"ip":ip,"time":str(int(time.time()*1000))})
	return jumptext

if __name__ == '__main__':

	app.run(host='0.0.0.0',debug=True,port=int(sys.argv[1]))
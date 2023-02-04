from flask import Flask,request,send_file
import sys,time,sqlite3



conn = sqlite3.connect('./flask-getip/ip.db', check_same_thread=False)
cur = conn.cursor()







jumptext='跳转失败，您可能开启了代理或者出现了未知错误'

app = Flask(__name__)

@app.route('/getquick/')
def adminget2():
	cur.execute("SELECT ip,unixtime FROM IP where id='quickjump'")
	return str(cur.fetchall())

@app.route('/get/')
def adminget():
	passwd = request.args.get('pwd')
	if (passwd == '5buW6ZuF6aao'):
		return send_file(r'./flask-getip/ip.db')
	return '密码错误'

@app.route('/admin/')
def admin():
	passwd = request.args.get('pwd')
	cur.execute('SELECT id FROM pwds WHERE pwd = "'+passwd+'"')
	okid=cur.fetchall()
	if (len(okid) >= 1):
		cur.execute("SELECT unixtime,ip FROM IP where id='"+okid[0][0]+"'")
		return str(cur.fetchall())
	else:
		return '不可用的密码'

@app.route('/execute/')
def adminshow():
	passwd = request.args.get('pwd')
	if (passwd == '5buW6ZuF6aao'):
		cur.execute(request.args.get('cmd'))
		return str(cur.fetchall())
	return '密码错误'

@app.route('/clear/')
def clear():
	passwd = request.args.get('pwd')
	if (passwd == '5buW6ZuF6aao'):
		cur.execute('DELETE FROM IP;')
		conn.commit()
		return 'delete!'
	return '密码错误'

@app.route('/changetext/')
def changetext():
	global jumptext
	passwd = request.args.get('pwd')
	if (passwd == '5buW6ZuF6aao'):
		jumptext=request.args.get('text')
		return '修改成功！'
	return '密码错误！'

@app.route('/jump/')
def jumpa():
	id = request.args.get('jumpid')
	ip = request.remote_addr
	x = """
	INSERT INTO ip ('unixtime','id','ip')
	VALUES(?,?,?)
	"""
	y = [(int(time.time()*1000),id,ip)]
	cur.executemany(x,y)
	conn.commit()
	return jumptext

if __name__ == '__main__':

	app.run(host='0.0.0.0',debug=True,port=int(sys.argv[1]))
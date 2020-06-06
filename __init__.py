from flask import Flask, render_template, redirect, request
import gspread
import random

gc = gspread.service_account(filename='D:\\file.json')
app = Flask(__name__)

sh = gc.open("Auction")
sheet1 = sh.get_worksheet(0)

col0 = sheet1.col_values(1)
col1 = sheet1.col_values(2)
col2 = sheet1.col_values(3)
col3 = sheet1.col_values(4)
col4 = sheet1.col_values(5)

# POSITION DEFINITIONS 

players = []
curPos = ""
goToNext = False
poslist = []
player = []
def getNewPos():
	global poslist
	global curPos
	firstPos = random.choice(poslist)
	poslist.remove(firstPos)
	curPos = firstPos
def getPlayer():
	global players
	global player
	global poslist
	global curPos
	#searchTerm = pos
	curList = []
	for i in range(0,len(players)):
		if (players[i][4] == curPos):
			curList.append(players[i])
	if (len(curList) == 0):
		getNewPos()
		curList = []
		for i in range(0,len(players)):
			if (players[i][4] == curPos):
				curList.append(players[i])

	thing = random.choice(curList)
	players.remove(thing)		
	player = thing

def update(p,t,b):
	row = str((p[5] + 1))
	theid = "G" + row
	theid2 = "F" + row
	sheet1.update(theid,b)
	sheet1.update(theid2,t)
@app.before_first_request
def createSheet():
	global poslist
	global players
	global curPos
	global player
	for i in range(1,len(col1)):
		players.append([col1[i],col2[i],col3[i],col4[i],col0[i],i])
	poslist = ["GK-1","GK-2","GK-3","LB-1","LB-2","LB-3","RB-1","RB-2","RB-3","CB-1","CB-2","CB-3","CDM-1","CDM-2","CAM-1","CAM-2","CM-1","CM-2","CM-3","CM-4","RM","LM","RW-1","RW-2","LW-1","LW-2","CF","LF","ST-1","ST-2","ST-3","ST-4","ST-5"]
	firstPos = random.choice(poslist)
	poslist.remove(firstPos)
	curPos = firstPos
	getPlayer()
@app.route('/')
def index():
	return("koulutos")
@app.route('/auction')
def auction():
	#global curPos
	#global goToNext
	global player
	return render_template("index.html", currentPlayerName=player[1], currentPosition=player[0], currentRating=player[2],currentBid=player[3], curPos = curPos)
@app.route('/auctioncontrol')
def auctionControl():
	global player
	return render_template("panel.html", currentPlayerName=player[1], currentPosition=player[0], currentRating=player[2],currentBid=player[3], curPos = curPos)
@app.route('/acontrolpanelactionhandler',methods = ['POST', 'GET'])
def handler1():
	tName = request.args.get("teamname")
	tBid = request.args.get("finalbid")
	update(player,tName,tBid)
	getPlayer()
	return redirect("/auctioncontrol",code=302)

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')
	
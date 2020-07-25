from flask import Flask, render_template, redirect, request
import gspread
import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from math import pi
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import time

gc = gspread.service_account(filename='D:\\file.json')

app = Flask(__name__)


playerstats = []
position_primary = []
#positions_secondary = []

sh = gc.open("FINAL")
sheet1 = sh.worksheet("FINAL")
fs = sh.worksheet("Finances")
'''
short_names = sheet1.col_values(3)
long_names = sheet1.col_values(4)
age = sheet1.col_values(5)
start_price = sheet1.col_values(6)
nationality = sheet1.col_values(10)
overall_rating = sheet1.col_values(12)
position = sheet1.col_values(16)
for i in range(0,len(position)-1):
	positions_player = position[i].split(".")
	if len(positions_player) > 1:
		position_primary.append(positions_player[0])
		positions_secondary.append(positions_player[1:(len(positions_player)-1)])
	else:
		position_primary.append(positions_player[0])
pref_foot = sheet1.col_values(17)
weak_foot = sheet1.col_values(18)
skill_moves = sheet1.col_values(19)
work_rate = sheet1.col_values(20)
time.sleep(10)
pac = sheet1.col_values(32)
sho = sheet1.col_values(33)
pas = sheet1.col_values(34)
dri = sheet1.col_values(35)
defe = sheet1.col_values(36)
phy = sheet1.col_values(37)
time.sleep(10)
gkd = sheet1.col_values(38)
gkh = sheet1.col_values(39)
gkk = sheet1.col_values(40)
gkr = sheet1.col_values(41)
gks = sheet1.col_values(42)
gkp = sheet1.col_values(43)

plt = sheet1.col_values(44)
for i in range(44,105):
	playerstats.append(sheet1.col_values(i))
'''

fullsheet = sheet1.batch_get(["AllValues"])[0]
gks = fullsheet[0:25]
players = fullsheet[25:len(fullsheet)]
for i in range(0,(len(players))):
	splitVal = players[i][13].split(",")
	if len(splitVal) > 1:
		players[i][13] = splitVal[0]
		players[i].append(splitVal[1:])
	else:
		pass
col_headers = sheet1.batch_get(["ColHeaders"])

# POSITION DEFINITIONS 

#p#layers = []
curPos = ""
#goToNext = False
poslist = []
player = []
isGK = False
matplotlib_data = ""
currentImage = ""
teams = ["United","Real","Barcelona","Chelsea","Dortmund","City","Piemonte","Kaisa","PSG","Atletico","Unsold"]
indexedTeams = {"Real":["B","C",3],"United":["D","E",3],"Barcelona":["F","G",3],"Kaisa":["H","I",3],"Chelsea":["J","K",3],"Piemonte":["L","M",3],"PSG":["N","O",3],"Dortmund":["P","Q",3],"City":["R","S",3],"Atletico":["T","U",3],"Unsold":["V","W",3]}
#                               N    V  Va,
financesTeams = {}
def getFinances():
	for i in indexedTeams.keys():
		finVal = indexedTeams[i][1]+"2"
		financesTeams[i] = fs.acell(finVal).value


def getNewPos(newPos):
	global poslist
	global curPos
	global isGK
	if newPos == "":
		firstPos = random.choice(poslist)
		curPos = firstPos
	elif newPos in poslist:
		curPos = newPos
		if curPos == "GK":
			isGK = True
		else:
			isGK = False
		getPlayer()
	if curPos == "GK":
		isGK = True
	else:
		isGK = False

def getPlayer():
	global players
	global player
	global poslist
	global curPos
	global isGK
	#searchTerm = pos
	curList = []
	if not isGK:
		for i in range(0,len(players)):
			if (players[i][13] == curPos):
				curList.append(players[i])
	elif isGK:
		curList = gks
	if (len(curList) == 0):
		poslist.remove(curPos)
		getNewPos("")
		curList = []
		if not isGK:
			for i in range(0,len(players)):
				if (players[i][13] == curPos):
					curList.append(players[i])
		elif isGK:
			curList = gks
	try:
		thing = random.choice(curList)
	except:
		if (len(curList) == 0):
			poslist.remove(curPos)
			getNewPos("")
			curList = []
			if not isGK:
				for i in range(0,len(players)):
					if (players[i][13] == curPos):
						curList.append(players[i])
			elif isGK:
				curList = gks
		thing = random.choice(curList)
	if isGK:
		gks.remove(thing)
	else:
		players.remove(thing)		
	player = thing
	draw_matplotlib_graph()

def draw_matplotlib_graph():
	global isGK
	global player
	global currentImage
	fig = plt.figure(figsize=(3.5,3))
	ax = plt.subplot(polar="True")
	if not isGK:
		categories = ['PAC','SHO','PAS','DRI', 'DEF','PHY']
		values = [int(player[30]),int(player[31]), int(player[32]),int(player[33]),int(player[34]),int(player[35])]
		for i in range(0,(len(values))):
			categories[i] = categories[i] + " "+str(values[i])
	else:
		categories = ['GKD','GKH','GKK','GKR','GKS','GKP']
		values = [int(player[36]),int(player[37]), int(player[38]),int(player[39]),int(player[40]),int(player[41])]
		for i in range(0,(len(values))):
			categories[i] = categories[i] + " "+str(values[i])
	N = len(categories)
	values += values[:1]
	angles = [n/float(N) * 2 * pi for n in range(N)]
	angles += angles[:1]
	plt.polar(angles,values)
	plt.fill(angles, values, alpha=0.3)
	plt.xticks(angles[:-1],categories)
	ax.set_rlabel_position(0)
	pngImage = io.BytesIO()
	FigureCanvas(fig).print_png(pngImage)
	pngImageB64String = "data:image/png;base64,"
	pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
	currentImage = pngImageB64String




def update(p,t,b):  # TO BE FIXED FOR NEW FORMAT
	global indexedTeams
	'''
	row = str((p[5] + 1))
	theid = "G" + row
	theid2 = "F" + row
	sheet1.update(theid,b)
	sheet1.update(theid2,t)
	'''
	pName = p[0]
	pNameCell = indexedTeams[t][0]+str(indexedTeams[t][2])
	pPriceCell = indexedTeams[t][1]+str(indexedTeams[t][2])
	fs.update(pNameCell,pName)
	fs.update(pPriceCell,b)
	indexedTeams[t][2] += 1


@app.before_first_request
def createSheet():
	global poslist
	global players
	global curPos
	global player
	'''
	for i in range(0,len(short_names)-1):
		
		if position_primary == "GK": 
			toAppend = [i,short_names[i],long_names[i],age[i],start_price[i],nationality[i],overall_rating[i],position_primary[i],positions_secondary[i],pref_foot[i],weak_foot[i],skill_moves[i],work_rate[i],gkd[i],gkh[i],gkk[i],gkr[i],gks[i],gkp[i]]
			for k in range(0,len(playerstats)-1):
				toAppend.append(playerstats[k][i])
				players.append(toAppend)
		else:
			toAppend = [i,short_names[i],long_names[i],age[i],start_price[i],nationality[i],overall_rating[i],position_primary[i],positions_secondary[i],pref_foot[i],weak_foot[i],skill_moves[i],work_rate[i],pac[i],sho[i],dri[i],pas[i],defe[i],phy[i]]
			for k in range(0,len(playerstats)-1):
				toAppend.append(playerstats[k][i])
				gks.append(toAppend)
		'''
		# That's just something to help me keep track of the elements of that array. 	
	poslist = ['GK','LB','RB','CB','CDM','LWB','RWB','CM','CAM','LM','RM','CF','LW','RW','ST']
	firstPos = random.choice(poslist)
	#poslist.remove(firstPos)
	curPos = firstPos
	getPlayer()
	getFinances()

@app.route('/')
def index():
	return render_template("mindex.html")

@app.route('/auction')
def auction():
	global player
	return render_template("index.html", player=player,currentImage = currentImage,colValues=col_headers,lengthVal=int(len(col_headers)))

@app.route('/auctioncontrol')
def auctionControl():
	global player
	global poslist
	global teams
	return render_template("panel.html", player=player, currentImage = currentImage, poslist=poslist,teams=teams)

@app.route('/acontrolpanelactionhandler',methods = ['POST', 'GET'])
def handler1():
	tName = request.form["teamname"]
	tBid = request.form["finalbid"]
	update(player,tName,tBid)	
	getPlayer()
	return redirect("/auctioncontrol",code=302)
@app.route('/tracheselect', methods=['POST','GET'])
def handler2():
	trancheselect = request.args.get("trancheselect")
	getNewPos(str(trancheselect))
	return redirect("/auctioncontrol",code=302)

@app.route('/finances')
def finance_checker():
	getFinances()
	return(financesTeams)
if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')
	
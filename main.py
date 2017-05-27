from PySide import QtCore, QtGui

from MainWindow import Ui_MainWindow
import os, sys, time

app = QtGui.QApplication(sys.argv)
mainWindow = QtGui.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(mainWindow)

associatedLabels = {
	'200': {'title': ui.room200title, 'speaker': ui.room200speaker},
	'201': {'title': ui.room201title, 'speaker': ui.room201speaker},
	'208': {'title': ui.room208title, 'speaker': ui.room208speaker},
}

sessions = []
images = []

def loadImages():
	path = 'images/'
	fileList = [ f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) ]
	for imageFile in fileList:
		images.append(QtGui.QPixmap(path + imageFile))

def loadSessions():
	sessionDict = {}
	with open('schedule.tab', 'r') as scheduleFile:
		for line in scheduleFile:
			if line[0] != '#':
				parts = line.strip().split('\t')
				parts[0] = int(parts[0])
				if parts[0] not in sessionDict:
					sessionDict[parts[0]] = {}
				sessionDict[parts[0]][parts[1]] = parts[2:]

	sessionTimes = list(sessionDict.keys())
	sessionTimes.sort()
	for timestamp in sessionTimes:
		session = {
			'time': timestamp,
			'rooms': sessionDict[timestamp]
		}
		sessions.append(session)
		import datetime
		t = datetime.datetime.fromtimestamp(session['time']).strftime('%Y-%m-%d %H:%M:%S')
		print("Session check: " + t)
		for r in session['rooms']:
			print('\t%s\t%s' % (r, session['rooms'][r]))

def update():
	currentTime = int(time.time())# + 27*60*60 + 715*60
	ui.clock.setText(time.strftime('%H:%M:%S'))
	while len(sessions) > 0 and (currentTime - 11*60) > int(sessions[0]['time']):
		sessions.pop(0)

	if len(sessions) > 0:
		session = sessions[0]
		minutesLeft = int((session['time'] - currentTime)/60)
		ui.nextSession.setText('Next session in %dm' % minutesLeft)
		for room in associatedLabels.keys():
			if room in session['rooms']:
				associatedLabels[room]['title'].setText(session['rooms'][room][0])
				associatedLabels[room]['speaker'].setText(session['rooms'][room][1])
			else:
				associatedLabels[room]['title'].setText('<html>&nbsp;<br/>&nbsp;</html>')
				associatedLabels[room]['speaker'].setText('<html>&nbsp;</html>')
	else:
		pass

	if currentTime % 4 == 0:
		images.append(images.pop(0))
		ui.logo.setPixmap(images[0])

def startTimer():
	timer = QtCore.QTimer(mainWindow)
	timer.timeout.connect(update)
	timer.start(1000)

loadImages()
loadSessions()
startTimer()
mainWindow.show()
sys.exit(app.exec_())

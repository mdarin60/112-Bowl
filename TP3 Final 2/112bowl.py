from cmu_graphics import *
import math
import copy
import random
import csv
from PIL import Image
import os, pathlib
from datetime import date


#Creates Class for Time Button
class TimeButton:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.selected = False
        self.time = 10
        self.max = 180

    def select(self):
        self.selected = not self.selected

    def addTime(self):
        if self.time != self.max:
            self.time += 10
    
    def removeTime(self):
        if self.time != 10:
            self.time -= 10

    def isClicked(self, x, y):
        left = self.x - self.width/2
        right = self.x + self.width/2
        top = self.y - self.height/2
        bottom = self.y + self.height/2
        return (x > left and x < right and y > top and y < bottom)

def openImage(fileName):
    return Image.open(os.path.join(pathlib.Path(__file__).parent,fileName))

#Class for defenders
class Defender:
    def __init__(self, acc, speed, catchRadius, name, assignment):
        self.acc = acc
        self.speed = speed
        self.pos = [0,0]
        self.accVector = [0,0]
        self.veloc = [0, 0]
        self.name = name
        self.catchRadius = catchRadius
        #This takes in an instance of the wide receiver class
        self.assignment = assignment
        self.spriteIndex = [0,1]
    def __eq__(self, other):
        if isinstance(other, Defender) and self.name == other.name:
            return True
        else:
            return False


#Class for receivers
class Receiver:
    def __init__(self, acc, speed, catchRadius, name, key):
        self.acc = acc
        self.speed = speed
        self.pos = [0,0]
        self.accVector = [0,0]
        self.veloc = [0, 0]
        self.catchRadius = catchRadius
        self.name = name
        self.key = key
        self.spriteIndex = [0,0]

    def __eq__(self, other):
        if isinstance(other, Receiver) and self.name == other.name:
            return True
        else:
            return False
 #Class For Quarterbacks   
class Quarterback:
    def __init__(self, acc, speed, throwPower, throwAccuracy, name):
        self.acc = acc
        self.speed = speed
        self.pos = [0,0]
        self.accVector = [0,0]
        self.veloc = [0, 0]
        self.power = throwPower
        self.accuracy = throwAccuracy
        self.name = name
        self.spriteIndex = [0,0]

    def __eq__(self, other):
        if isinstance(other, Quarterback) and self.name == other.name:
            return True
        else:
            return False


#Function to switch teams during the game
def switchTeams(app, isTurnover):
    if app.teamOnOffense == 1:
        app.teamOnOffense = 2
        app.selectedTeamIndex = app.selectedTeam2Index
        
    else:
        app.teamOnOffense = 1
        app.selectedTeamIndex = app.selectedTeam1Index
    selectedTeam = app.teamList[app.selectedTeamIndex]
    app.wr1 = app.teamRosters[selectedTeam]['wr1']
    app.wr2 = app.teamRosters[selectedTeam]['wr2']
    app.te = app.teamRosters[selectedTeam]['te']
    app.rb = app.teamRosters[selectedTeam]['rb']
    app.qb = app.teamRosters[selectedTeam]['qb']
    app.receiverList = [app.wr1, app.wr2, app.te, app.rb]
    app.playerList = app.receiverList + [app.qb]
    app.defender1.assignment = app.wr1
    app.defender2.assignment = app.wr2
    app.defender3.assignment = app.te
    app.defender4.assignment = app.rb
    app.down = 1
    app.toGo = 110
    if isTurnover:
        app.lineOfScrimmage = 1200 - app.lineOfScrimmage
    else:
        app.lineOfScrimmage = app.driveStartX

def onAppStart(app):
    #Dictionaries where key corresponds to the path the key will take
    play1 = {
    'wr1': [(-100, 0), (-100, 0), (-50, -50)],
    'wr2': [(-100, 10), (-100, 0), (-50, 50)],
    'te': [(-100, 0), (-100, 0), (-50, 50)],
    'rb': [(0, 100), (-100, 0), (-100, 0)]
    }
    play2 = {
    'wr1': [(-150, 0), (20, 0)],
    'wr2': [(-150, 0), (20, 0)],
    'te': [(-150, 0), (20, 0)],
    'rb': [(-150, 0), (20, 0)]
    }
    play3 = {
    'wr1': [(-20, 0), (-20, -60), (-20, -60)],
    'wr2': [(-20, 10), (-20, 60), (-20, 60)],
    'te': [(-20, 0), (-20, 60), (-20, 60)],
    'rb': [(0, 20), (0, 80), (-100, 0)]
    }
    play4 = {
    'wr1': [(-600, 0)],
    'wr2': [(-600, 0)],
    'te': [(-600, 0)],
    'rb': [(-600, 0)]
    }
    play5 = {
    'wr1': [(-150, 0), (0, -150)],
    'wr2': [(-150, 10), (0, 150)],
    'te': [(-150, 0), (0, 150)],
    'rb': [(0, 100), (-150, 0)]
    }
    play6 = {
    'wr1': [(-150, 0), (-25, 25)],
    'wr2': [(-150, 0), (-25, -25)],
    'te': [(-150, 0), (-25, 25)],
    'rb': [(-100, 100), (-100, -100)]
    }
    app.playbook = {
        'play1': play1,
        'play2': play2,
        'play3': play3,
        'play4': play4,
        'play5': play5,
        'play6': play6
    }
    patriotsRoster = {
        'wr1': Receiver(.25, 6.5, 60,'K. Bourne', 'wr1'),
         'wr2': Receiver(.25, 6, 55, 'D. Douglas', 'wr2'),
         'te': Receiver(.25, 5.5, 65,'H. Henry', 'te'),
        'rb': Receiver(.25, 6.5, 50,'R. Stevenson', 'rb'),
        'qb': Quarterback(.15, 4.5, 400, 30, 'M. Jones')
    }
    dolphinsRoster = {
        'wr1': Receiver(.35, 7, 60,'T. Hill','wr1'),
         'wr2': Receiver(.3, 6.76, 55,'J. Waddle', 'wr2'),
         'te': Receiver(.2, 5.5, 50,'T. Conner','te'),
        'rb': Receiver(.3, 6.75, 40,'D. Achane','rb'),
        'qb': Quarterback(.3, 5, 550, 20, 'T. Tagovailoa')
    }
    billsRoster = {
        'wr1': Receiver(.25, 6.5, 50,'S. Diggs','wr1'),
         'wr2': Receiver(.25, 6, 50,'G. Davis','wr2'),
         'te': Receiver(.25, 5.5, 50,'D. Kincaid','te'),
        'rb': Receiver(.25, 6, 50,'J. Cook','rb'),
        'qb': Quarterback(.2, 5.5, 650, 28, 'J. Allen')
    }
    jetsRoster = {
        'wr1': Receiver(.2, 6.5, 50,'G. Wilson','wr1'),
         'wr2': Receiver(.5, 6.25, 50,'J. Brownlee','wr2'),
         'te': Receiver(.2, 6, 50,'T. Conklin','te'),
        'rb': Receiver(.1, 6.3, 50,'B. Hall','rb'),
        'qb': Quarterback(.2, 4.75, 600, 20, 'A. Rodgers')
    }
    app.teamRosters = {
        'Patriots': patriotsRoster,
        'Dolphins': dolphinsRoster,
        'Bills': billsRoster,
        'Jets': jetsRoster
    }
    app.timeButton = TimeButton(600, 550, 250, 100)
    #Sets dimensions of app
    app.height = 600
    app.width = 1200
    #Loads the records CSV file
    loadRecords(app)
    #Creates instances for defender
    app.defender1 = Defender(.5, 6.5, 45, 'CB1', None)
    app.defender2 = Defender(.5, 6.4, 40, 'CB2', None)
    app.defender3 = Defender(.5, 6.3, 35, 'CB3', None)
    app.defender4 = Defender(.3, 6, 30, 'LB', None)
    app.safety = Defender(.5, 6.5, 45, 'S', None)
    app.spy = Defender(.3, 6, 50, 'LB2', None)
    app.defenderList = [app.defender1, app.defender2, app.defender3, app.defender4, app.safety, app.spy]
    #Some values which are going to be used in later functions
    app.routeIndex = None
    app.selectedPlayer = None
    app.lastWR1Cords = None
    app.isPassing = False
    app.isRunning = False
    app.ballCords = [0,0]
    app.ballVeloc = [0,0]
    app.ballAccVector = [0, 0]
    app.ballAcc = 0
    app.ballYVeloc = 0
    app.ballYVelocVector = [0, 0]
    app.ballInAir = False
    app.targetCords = None
    app.isPaused = True
    app.betweenPlays = False
    app.message = ''
    app.ballHeight = 0
    app.targetReceiver = None
    app.ballTarget = None
    app.selectedPlay = None
    app.playChoiceScreen = False
    app.isGoingDown = False
    app.driveStartX = 880
    app.lineOfScrimmage = app.driveStartX
    app.startScreen = True
    app.selectedTeam1Index = 0
    app.selectedTeam2Index = 0
    app.selectedTeamIndex = 0
    app.teamList = ['Patriots', 'Jets', 'Bills', 'Dolphins']
    app.team2Score = 0
    app.team1Score = 0
    app.team1Name = 'Team 1'
    app.team2Name = 'Team 2'
    app.teamScore = 0
    app.down = 1
    app.toGo = 110
    app.stepCounter = 0
    app.selectedDefenderIndex = 0
    app.teamOnOffense = 1
    app.quarter = 1
    app.quarterTime = 30
    app.timeToGo = app.quarterTime
    app.clockRunning = False
    app.gameOver = False
    app.nextQuarter = False
    app.bouncable = True
    app.stepspersecond = 60
    app.rushClock = 75
    app.recordsScreen = False
    app.stepCount = 0
    app.catchable = False
    loadImages(app)

    loadStats(app)
#Creates stats fro all the players
def loadStats(app):
    app.qb1Stats = {
        "Passing Yards": 0,
        "Completions": 0,
        "Attempts": 0,
        "Passing TDs": 0,
        'Rushing Yards': 0,
        'Rushing Attempts': 0,
        'Rushing TDs': 0,
        "INTs": 0
    }
    app.qb2Stats = copy.deepcopy(app.qb1Stats)
    app.team1WR1Stats = {
        "Targets": 0,
        "Receptions": 0,
        "Receiving TDs": 0,
        "Receiving Yards": 0
    }
    app.team2WR1Stats = copy.deepcopy(app.team1WR1Stats)
    app.team1WR2Stats = copy.deepcopy(app.team1WR1Stats)
    app.team2WR2Stats = copy.deepcopy(app.team1WR1Stats)
    app.team1TEStats = copy.deepcopy(app.team1WR1Stats)
    app.team2TEStats = copy.deepcopy(app.team1WR1Stats)
    app.team1RBStats = copy.deepcopy(app.team1WR1Stats)
    app.team2RBStats = copy.deepcopy(app.team1WR1Stats)

#Loads the Images
def loadImages(app):
    loadLogos(app)
    loadSprites(app)
    loadPlayImages(app)
    loadDecorations(app)

def loadRecords(app):
    app.recordsDict = dict()
    #Used https://www.youtube.com/watch?v=q5uM4VKywbA to help learn how to use CSV
    with open('gamerecords.csv', 'r') as csv_file:
        gameRecordsCSV = csv.reader(csv_file)
        next(gameRecordsCSV)
        for line in gameRecordsCSV:
            record = line[0]
            data = line[1:]
            app.recordsDict[record] = data

def loadDecorations(app):
    #Image from https://www.pngkit.com/png/detail/117-1173151_fireworks-pixel-fireworks-png.png 
    app.fireworkSprite = CMUImage(openImage('Images/fireworkSprite.png'))
    
def loadPlayImages(app):
    play1Image = CMUImage(openImage('Images/play1Sprite.png'))
    play2Image = CMUImage(openImage('Images/play2Sprite.png'))
    play3Image = CMUImage(openImage('Images/play3Sprite.png'))
    play4Image = CMUImage(openImage('Images/play4Sprite.png'))
    play5Image = CMUImage(openImage('Images/play5Sprite.png'))
    play6Image = CMUImage(openImage('Images/play6Sprite.png'))
    app.playImages = {
        'play1': play1Image,
        'play2': play2Image,
        'play3': play3Image,
        'play4': play4Image,
        'play5': play5Image,
        'play6': play6Image
    }

def loadSprites(app):
    #Images created using piskelapp.com, but are inspired from the sprites from the game retro bowl
    #Image of Retro Bowl Sprite here https://upload.wikimedia.org/wikipedia/en/b/bf/Retro_Bowl_cover.png
    #Other images that inspired me https://www.spriters-resource.com/mobile/retrobowl/sheet/200221/
    app.team1SpriteLeft= CMUImage(openImage('Images/team1Sprite.png'))
    app.team1SpriteLeft2 = CMUImage(openImage('Images/team1SpriteLeft2.png'))
    app.team1SpriteRight = CMUImage(openImage('Images/team1SpriteRight.png'))
    app.team1SpriteRight2 = CMUImage(openImage('Images/team1SpriteRight2.png'))
    app.team2SpriteLeft = CMUImage(openImage('Images/team2Sprite.png'))
    app.team2SpriteLeft2 = CMUImage(openImage('Images/team2SpriteLeft2.png'))
    app.team2SpriteRight = CMUImage(openImage('Images/team2SpriteRight.png'))
    app.team2SpriteRight2 = CMUImage(openImage('Images/team2SpriteRight2.png'))
    #Creates 2D List of sprites to be used for animation
    app.team1Sprites = [[app.team1SpriteLeft, app.team1SpriteRight], [app.team1SpriteLeft2, app.team1SpriteRight2]]
    app.team2Sprites = [[app.team2SpriteLeft, app.team2SpriteRight], [app.team2SpriteLeft2, app.team2SpriteRight2]]
    app.ballSprite = CMUImage(openImage('Images/ballSprite.png'))
    app.field = CMUImage(openImage('Images/field.png'))

def loadLogos(app):
    #Source for image https://freebiesupply.com/logos/new-england-patriots-logo/
    patriotsLogo = CMUImage(openImage("Images/new-england-patriots-logo-transparent.png"))
    #Source for image https://en.wikipedia.org/wiki/Logos_and_uniforms_of_the_New_York_Jets
    jetsLogo = CMUImage(openImage("Images/jetslogo.png"))
    #Source for image https://www.sportslogos.net/logos/view/n0fd1z6xmhigb0eej3323ebwq/Buffalo_Bills/1976/Primary_Logo
    billsLogo = CMUImage(openImage("Images/billslogo.png"))
    #Source for image https://seeklogo.com/vector-logo/287056/new-miami-dolphins 
    dolphinsLogo = CMUImage(openImage("Images/dolphinslogo.png"))
    app.logosDict = {
        'Patriots': [patriotsLogo, 240, 140],
        'Jets': [jetsLogo, 240, 140],
        'Bills': [billsLogo, 215, 140],
        'Dolphins': [dolphinsLogo, 200, 140]
    }

def startScreen(app):
    app.isPaused = True
    app.startScreen = True

def drawStartScreen(app):
    team1 = app.teamList[app.selectedTeam1Index]
    team2 = app.teamList[app.selectedTeam2Index]
    image1 = app.logosDict[team1][0]
    width1, height1 = app.logosDict[team1][1], app.logosDict[team1][2]
    image2 = app.logosDict[team2][0]
    width2, height2 = app.logosDict[team2][1], app.logosDict[team2][2]
    #Makes Screen Blue
    drawRect(0, 0, 1200, 600, fill='blue', border = 'black')
    #Draws team 1 label canvas
    drawRect(100, 300, 400, 200, fill='white', border='black')
    #Canvas for team 1 image
    drawRect(170, 150, 260, 160, fill='white', border='black')
    #Draws team 2 label canvas
    drawRect(700, 300, 400, 200, fill='white', border='black')
    #Canvas for team 2 image
    drawRect(770, 150, 260, 160, fill='white', border='black')
    #Draws team 1 label
    drawLabel(app.teamList[app.selectedTeam1Index], 300, 400, size=50, bold=True)
    #Draws team 2 label
    drawLabel(app.teamList[app.selectedTeam2Index], 900, 400, size=50, bold=True)
    #Draws team 1 image
    left1 = 300 - width1//2
    top1 = 230 - height1 // 2
    drawImage(image1, left1, top1, width=width1, height=height1)
    #Draws team 2 image
    left2 = 900 - width2//2
    top2 = 230 - height2 // 2
    drawImage(image2, left2, top2, width=width2, height=height2)
    #Title
    drawLabel('112 Bowl',600, 50, size = 100, bold=True)
    drawLabel('Used, a/d, and left and right arrow' ,600, 150, size = 20, bold=True)
    drawLabel('to choose teams.' ,600, 180, size = 20, bold=True)
    drawLabel('Press P to start' ,600, 210, size = 20, bold=True)
    drawLabel('Click the time buttom' ,600, 240, size = 20, bold=True)
    drawLabel('and use w/s to adjust' ,600, 270, size = 20, bold=True)
    drawRect(1050, 0, 150, 50, fill='Cyan', border='black')
    drawLabel('Records' ,1125, 25, size = 15, bold=True)
    #Draws time
    if app.timeButton.selected:
        borderColor = 'yellow'
    else:
        borderColor = 'black'
    drawRect(app.timeButton.x, app.timeButton.y, app.timeButton.width, app.timeButton.height, 
            align = 'center', fill='white', border=borderColor)
    seconds = app.timeButton.time % 60
    minutes = app.timeButton.time // 60
    if seconds < 10:
        seconds = f'0{seconds}'
    label = f'{minutes}:{seconds}'
    drawLabel(label, app.timeButton.x, app.timeButton.y, size=50, bold=True)

def drawPlayers(app):
    if app.teamOnOffense == 1:
        offenseImage = app.team1Sprites
        defenseImage = app.team2Sprites
    else:
        offenseImage = app.team2Sprites
        defenseImage = app.team1Sprites
    for player in app.playerList:
        sprite = offenseImage[player.spriteIndex[0]][player.spriteIndex[1]]
        if player == app.selectedPlayer:
            drawLabel(player.name, player.pos[0], player.pos[1]+20, bold=True)
        left = player.pos[0] - 32
        top = player.pos[1] - 32
        drawImage(sprite, left, top, width=64, height = 64)
        #drawCircle(player.pos[0], player.pos[1], 10, fill=offenseColor, border=offenseBorder)
    for i in range(len(app.defenderList)):
        defender = app.defenderList[i]
        sprite = defenseImage[defender.spriteIndex[0]][defender.spriteIndex[1]]
        if i == app.selectedDefenderIndex:
            drawLabel(defender.name, defender.pos[0], defender.pos[1]+20, bold=True)
        left = defender.pos[0] - 32
        top = defender.pos[1] - 32
        drawImage(sprite, left, top, width=64, height = 64)
    left = app.ballCords[0] - 16
    top = app.ballCords[1] - 16
    drawImage(app.ballSprite, left, top)

def drawScoreboard(app):
    drawRect(0, 550, 1200, 50, fill='black',border='grey')
    drawLine(270, 550, 270, 600, fill= 'grey', lineWidth=3)
    secondsLeft = app.timeToGo // 15
    team1Logo = app.logosDict[app.teamList[app.selectedTeam1Index]][0]
    team1Width = app.logosDict[app.teamList[app.selectedTeam1Index]][1]//3
    team1Height = app.logosDict[app.teamList[app.selectedTeam1Index]][2]//3
    top = 575 - team1Height//2
    team2Logo = app.logosDict[app.teamList[app.selectedTeam2Index]][0]
    team2Width = app.logosDict[app.teamList[app.selectedTeam2Index]][1]//3
    team2Height = app.logosDict[app.teamList[app.selectedTeam2Index]][2]//3
    drawImage(team1Logo, 315, top, width=team1Width, height=team1Height)
    drawLabel(f'Team 1: {app.team1Score}', 480, 575, size=35, fill='white',bold=True)
    top = 575 - team1Height//2
    drawImage(team2Logo, 600, top, width=team2Width, height=team2Height)
    drawLabel(f'Team 2: {app.team2Score}', 765, 575, size=35, fill='white',bold=True)
    drawLine(880, 550, 880, 600, fill= 'grey', lineWidth=3)
    drawLine(1000, 550, 1000, 600, fill= 'grey', lineWidth=3)
    drawLabel(str(app.quarter)+ending(app.quarter), 940, 575, fill = 'white', bold=True, size=35)
    minutesLeft = secondsLeft // 60
    secondsLeft %= 60
    if secondsLeft < 10:
        secondsLeft = '0'+str(secondsLeft)
    drawLabel(f'{minutesLeft}:{secondsLeft}', 1075, 575, fill = 'white', size=35, bold=True)
    drawLine(1150, 550, 1150, 600, fill = 'grey', lineWidth=3)
    secondsRushLeft = str(int(app.rushClock // 15))
    drawLabel(secondsRushLeft, 1175, 575, fill='white', size = 35, bold=True)
    yardsToGo = int(app.toGo // 11)
    if yardsToGo == 0:
        yardsToGo = 'Inches'
    if app.toGo > app.lineOfScrimmage - 50:
        yardsToGo = 'Goal'
    convertNumberToString = {1: '1st', 2: '2nd', 3: '3rd', 4: '4th'}
    down = convertNumberToString[app.down]
    drawLabel(f'{down} and {yardsToGo}', 135, 575, size=35, fill='white', bold=True)

#Used to help generate strings
def ending(n):
    endingDict = {
        1: 'st',
        2: 'nd',
        3: 'rd',
        4: 'th'
    }
    return endingDict[n]

def drawField(app):
    #Draws Field
    drawImage(app.field, 0, 0, width=1200, height=600)
    #Draws line of scrimmage and first down Line
    drawLine(app.lineOfScrimmage, 50, app.lineOfScrimmage, 550, lineWidth=5)
    drawLine(app.lineOfScrimmage-app.toGo, 50, app.lineOfScrimmage-app.toGo, 550, fill ='yellow', lineWidth=5)
    

def drawPlaybook(app):   
    for i in range(2):
        for j in range(3):
            drawRect(j*400, i*275, 400, 275, fill='black', border='grey')
            playNumber = (i*3)+(j+1)
            playString = f'play{playNumber}'
            playImage = app.playImages[playString]
            drawImage(playImage, j*400, i*275)
   

def drawTarget(app):
    drawCircle(app.targetCords[0], app.targetCords[1], app.qb.accuracy, fill=None, border='black')

def drawPlayEndScreen(app):
    drawRect(0, 200, 1200, 200, fill='black',border='grey')
    drawLabel(app.message, 600, 285, size=60, bold=True, fill='white')
    drawLabel("Press space to continue", 600, 365, size=20, bold=True, fill='white')

def drawGameOverScreen(app):
    drawRect(0, 0, 1200, 600, fill='black', border = 'grey')
    victor = None
    if app.team1Score > app.team2Score:
        victor = app.team1Name
        loser = app.team2Name
    elif app.team1Score < app.team2Score:
        victor = app.team2Name
        loser = app.team1Name
    if victor == None:
        drawLabel(f'{app.team1Name} tied {app.team2Name} with the score:', 600, 200, size=50, bold=True, fill='white')
        drawLabel(f'{app.team1Score}-{app.team2Score}', 600, 400, size=50, bold=True, fill='white')
    else:
        winningScore = max(app.team1Score, app.team2Score)
        losingScore = min(app.team1Score, app.team2Score)
        drawImage(app.fireworkSprite, 600, 300, align='center')
        drawRect(600, 300, 500, 300, align='center', fill='black',border='grey')
        drawLabel(f'{victor} beats {loser}', 600, 200, size=50, bold=True, fill = 'white')
        drawLabel(f'with the score:', 600, 250, size=50, bold=True, fill = 'white')
        drawLabel(f'{winningScore}-{losingScore}', 600, 350, size=50, bold=True, fill = 'white')

def drawRecordsScreen(app):
    drawRect(0, 0, 1200, 600, fill='blue', border = 'black')
    recordList = ['Points', 'Passing TDs', 'Passing Yards', 'Completions', 'Attempts', 'Rushing Yards', 
                  'Rushing Attempts', 'Rushing TDs', 'INTs', 'Targets', 'Receptions', 'Receiving TDs', 'Receiving Yards']
    for i in range(1, 14):
        drawLine(0, i*46, 1200, i*46, lineWidth=3)
    for i in range(1, 4):
        drawLine(300*i, 0, 300*i, 600, lineWidth=3)
    for i in range(len(recordList)):
        record = recordList[i]
        player = app.recordsDict[record][0]
        number = app.recordsDict[record][1]
        date = app.recordsDict[record][2]
        drawLabel(record, 150, 23+i*46, size=20, bold=True)
        drawLabel(player, 450, 23+i*46, size=20, bold=True)
        drawLabel(number, 750, 23+i*46, size=20, bold=True)
        drawLabel(date, 1050, 23+i*46, size=20, bold=True)


    


def redrawAll(app):
    if not app.startScreen and not app.recordsScreen:
        drawField(app)
        drawPlayers(app)
        drawScoreboard(app)
        if app.isPassing and app.targetCords != None:
            drawTarget(app)
    if app.betweenPlays:
        drawPlayEndScreen(app)
    if app.playChoiceScreen:
        drawPlaybook(app)
        drawScoreboard(app)
    if app.startScreen:
        drawStartScreen(app)  
    if app.gameOver:
        drawGameOverScreen(app)
    if app.recordsScreen:
        drawRecordsScreen(app)
#Makes sure that user can catch ball in stride and receiver will not stop
def onKeyHold(app, key):
    if not app.isPaused and not app.ballInAir and (app.isPassing or app.isRunning):
        selectedDefender = app.defenderList[app.selectedDefenderIndex]
        if ('w' in key and app.teamOnOffense == 1) or (('t' in key or "up" in key) and app.teamOnOffense == 2):
            app.selectedPlayer.accVector[1] = -1*app.selectedPlayer.acc
        if ('s' in key and app.teamOnOffense == 1) or (('g' in key or 'down' in key) and app.teamOnOffense == 2):
            app.selectedPlayer.accVector[1] = app.selectedPlayer.acc
        if ('a' in key and app.teamOnOffense == 1) or (('f' in key or 'left' in key) and app.teamOnOffense == 2):
            app.selectedPlayer.accVector[0] = -1*app.selectedPlayer.acc
        if ('d' in key and app.teamOnOffense == 1) or (('h' in key or 'right' in key) and app.teamOnOffense == 2):
            app.selectedPlayer.accVector[0] = app.selectedPlayer.acc
        if ('a' in key and app.teamOnOffense == 2) or (('f' in key or 'left' in key) and app.teamOnOffense == 1):
            selectedDefender.accVector[0] = -1*selectedDefender.acc
        if ('d' in key and app.teamOnOffense == 2) or (('h' in key or 'right' in key) in key and app.teamOnOffense == 1):
            selectedDefender.accVector[0] = selectedDefender.acc
        if ('s' in key and app.teamOnOffense == 2) or (('g' in key or 'down' in key) in key and app.teamOnOffense == 1):
            selectedDefender.accVector[1] = selectedDefender.acc
        if ('w' in key and app.teamOnOffense == 2) or (('t' in key or "up" in key) in key and app.teamOnOffense == 1):
            selectedDefender.accVector[1] = -1*selectedDefender.acc
#Used to control players
def onKeyPress(app, key):
    if key == 'space' and app.gameOver:
        app.startScreen = True
        app.gameOver = False
    if not app.isPaused:
        if key == 'space' and not app.isPassing and not app.isRunning:
            getInFormation(app)
            app.fieldDrawn = True
            app.bouncable = True
            app.isGoingDoing = False
            app.routeIndex = 0
            app.lastWR1Cords = copy.copy(app.wr1.pos)
            app.isPassing = True
        #Movement triggers
        if app.isPassing == True or app.isRunning == True:
            selectedDefender = app.defenderList[app.selectedDefenderIndex]
            if (key == 'w' and app.teamOnOffense == 1) or ((key == 't' or key == 'up')  and app.teamOnOffense == 2):
                app.selectedPlayer.accVector[1] = -1*app.selectedPlayer.acc
            if (key == 's' and app.teamOnOffense == 1) or ((key == 'g' or key == 'down') and app.teamOnOffense == 2):
                app.selectedPlayer.accVector[1] = app.selectedPlayer.acc
            if (key == 'a' and app.teamOnOffense == 1) or ((key == 'f' or key == 'left') and app.teamOnOffense == 2):
                app.selectedPlayer.accVector[0] = -1*app.selectedPlayer.acc
            if (key == 'd' and app.teamOnOffense == 1) or ((key == 'h' or key == 'right') and app.teamOnOffense == 2):
                app.selectedPlayer.accVector[0] = app.selectedPlayer.acc
            if (key == 'a' and app.teamOnOffense == 2) or ((key == 'f' or key == 'left') and app.teamOnOffense == 1):
                selectedDefender.accVector[0] = -1*selectedDefender.acc
            if (key == 'd' and app.teamOnOffense == 2) or ((key == 'h' or key == 'right') and app.teamOnOffense == 1):
                selectedDefender.accVector[0] = selectedDefender.acc
            if (key == 's' and app.teamOnOffense == 2) or ((key == 'g' or key == 'down') and app.teamOnOffense == 1):
                selectedDefender.accVector[1] = selectedDefender.acc
            if (key == 'w' and app.teamOnOffense == 2) or ((key == 't' or key == 'up')  and app.teamOnOffense == 1):
                selectedDefender.accVector[1] = -1*selectedDefender.acc
        
    elif app.betweenPlays and key == 'space':
        app.betweenPlays = False
        app.message = ''
        app.selectedPlayer = None
        choosePlay(app)
    elif app.startScreen:
        if key == 'a':
            if app.selectedTeam1Index != 0:
                app.selectedTeam1Index -= 1
            else:
                app.selectedTeam1Index = len(app.teamList) -1
        if key == 'd':
            if app.selectedTeam1Index != len(app.teamList) -1:
                app.selectedTeam1Index += 1
            else:
                app.selectedTeam1Index = 0
        if key == 'f' or key == 'left':
            if app.selectedTeam2Index != 0:
                app.selectedTeam2Index -= 1
            else:
                app.selectedTeam2Index = len(app.teamList) -1
        if key == 'h' or key == 'right':
            if app.selectedTeam2Index != len(app.teamList) -1:
                app.selectedTeam2Index += 1
            else:
                app.selectedTeam2Index = 0
        if key == 'p':
            initiateGame(app)
        if key == 'w' and app.timeButton.selected:
            app.timeButton.addTime()
        if key == 's' and app.timeButton.selected:
            app.timeButton.removeTime()
            
    if key == 'b':
        if app.selectedDefenderIndex != len(app.defenderList) - 1:
            app.selectedDefenderIndex += 1
        else:
            app.selectedDefenderIndex = 0
        defender = app.defenderList[app.selectedDefenderIndex]
        defender.accVector = [0,0]

#Function to set variable to pre-game state, and to load the teams
def initiateGame(app):
    app.catchable = False
    app.startScreen = False
    app.selectedTeamIndex = app.selectedTeam1Index
    selectedTeam = app.teamList[app.selectedTeamIndex]
    app.wr1 = app.teamRosters[selectedTeam]['wr1']
    app.wr2 = app.teamRosters[selectedTeam]['wr2']
    app.te = app.teamRosters[selectedTeam]['te']
    app.rb = app.teamRosters[selectedTeam]['rb']
    app.qb = app.teamRosters[selectedTeam]['qb']
    #Creates lists to increase efficiency
    app.receiverList = [app.wr1, app.wr2, app.te, app.rb]
    app.playerList = app.receiverList + [app.qb]
    app.defender1.assignment = app.wr1
    app.defender2.assignment = app.wr2
    app.defender3.assignment = app.te
    app.defender4.assignment = app.rb
    app.spy.assignment = app.qb
    app.selectedPlayer = app.qb
    app.down = 1
    app.team1Score = 0
    app.team2Score = 0
    app.toGo = 110
    app.quarterTime = (app.timeButton.time) * 15
    app.timeToGo = app.quarterTime
    app.lineOfScrimmage = app.driveStartX
    app.quarter = 1
    app.teamOnOffense = 1
    choosePlay(app)

#Ensures that player comes to stop when user is not pressing key
def onKeyRelease(app, key):
    if not app.isPaused and app.selectedPlayer != None:
        selectedDefender = app.defenderList[app.selectedDefenderIndex]
        if (key in {'w', 's'} and app.teamOnOffense == 1) or (key in {'g', 't'} and app.teamOnOffense == 2):
            app.selectedPlayer.accVector[1] = 0
        if (key in {'a', 'd'} and app.teamOnOffense == 1) or (key in {'f', 'h'} and app.teamOnOffense == 2):
            app.selectedPlayer.accVector[0] = 0
        if (key in {'a', 'd'} and app.teamOnOffense == 2) or (key in {'f', 'h'} and app.teamOnOffense == 1):
            selectedDefender.accVector[0] = 0
        if (key in {'w', 's'} and app.teamOnOffense == 2) or (key in {'g', 't'} and app.teamOnOffense == 1):
            selectedDefender.accVector[1] = 0
        
            

def onMouseMove(app, mouseX, mouseY):
    if app.isPassing:
        dx = mouseX - app.qb.pos[0]
        dy = mouseY - app.qb.pos[1]
        targetXCord = mouseX
        if dx > 0:
            targetXCord = app.qb.pos[0]
            dx = 0
        if magnitude([dx, dy]) > app.qb.power:
            unitVector = [dx/magnitude([dx, dy]), dy/magnitude([dx, dy])]
            adjustedMagnitudeVector = [unitVector[0] * app.qb.power, unitVector[1] * app.qb.power]
            app.targetCords = [app.qb.pos[0] + adjustedMagnitudeVector[0], app.qb.pos[1] + adjustedMagnitudeVector[1]]
        else:
            app.targetCords = [targetXCord, mouseY]
    
def detectIfPressed(x, y, left, top, right, bottom):
    return (x < right and x > left) and (y > top and y < bottom)

def onMousePress(app, mouseX, mouseY):
    if app.startScreen and detectIfPressed(mouseX, mouseY, 1050, 0, 1200, 50):
        app.recordsScreen = True
        app.startScreen = False
    elif app.startScreen and app.timeButton.isClicked(mouseX, mouseY):
        app.timeButton.select()
    elif app.recordsScreen:
        app.recordsScreen = False
        app.startScreen = True
    if app.isPassing and app.targetCords != None:
        throwBall(app, mouseX, mouseY)
    elif app.playChoiceScreen:
        getInFormation(app)
        app.selectedPlayer = app.qb
        for receiver in app.receiverList:
            receiver.veloc = [0,0]
            receiver.accVector = [0,0]
        app.ballVeloc = [0,0]
        app.ballAccVector = [0,0]
        app.ballHeight = 0
        playChosen = getPlay(mouseX, mouseY)
        app.selectedPlay = app.playbook[playChosen]
        app.isPaused = False
        app.playChoiceScreen = False

#Gets play chosen from the click
def getPlay(x, y):
    col = (x // 400)+1
    row = (y//300)
    playNumber = (row*3)+col
    return f'play{playNumber}'

#Creates a point for the ball to throw to, and sets the ball's physics variable
def throwBall(app, mouseX, mouseY): 
    app.qb.accVector = [0,0]
    dx, dy = findRandomPointInCircle(app.qb.accuracy)
    app.ballTarget = [app.targetCords[0] + dx, app.targetCords[1] + dy]
    dx2 = app.ballTarget[0] - app.ballCords[0]
    dy2 = app.ballTarget[1] - app.ballCords[1]
    distance = magnitude([dx2, dy2])
    velocVectorX, velocVectorY, app.ballAccVector, app.ballYVeloc = getParabolaVars(distance, dx2, dy2)
    app.ballYVelocVector = velocVectorY
    app.ballVeloc = [velocVectorX[0] + velocVectorY[0], velocVectorX[1] + velocVectorY[1]]
    app.ballAcc = 2
    app.isPassing = False
    app.targetReceiver = getNearestReceiver(app)
    app.ballInAir = True
    app.isGoingDown = False
    app.catchable = True
    updateStatsOnThrow(app)

#Used for records purposes
def updateStatsOnThrow(app):
    qbStats = statsToAddTo(app, 'qb', app.teamOnOffense)
    receiverStats = statsToAddTo(app, app.targetReceiver.key, app.teamOnOffense)
    qbStats["Attempts"] += 1
    receiverStats["Targets"] += 1

def ballOutOfBounds(app):
    return app.ballCords[1] > 1150 or app.ballCords[1] < 50 


def getNearestDefender(app):
    closestDistance = 99999
    closestDefender = None
    for defender in app.defenderList:
        dx = app.ballCords[0] - defender.pos[0]
        dy = app.ballCords[1] - defender.pos[1]
        distance = magnitude([dx,dy])
        if distance < closestDistance:
            closestDistance = distance
            closestDefender = defender
    return closestDefender

#Determines if ball is caught or not, and then updates the game status
def catchBall(app):
    qbStats = statsToAddTo(app, 'qb', app.teamOnOffense)
    dxOffense, dyOffense = app.ballCords[0] - app.targetReceiver.pos[0], app.ballCords[1] - app.targetReceiver.pos[1]
    offenseDistance = int(magnitude([dxOffense, dyOffense]))
    closestDefender = getNearestDefender(app)
    dxDefense, dyDefense = app.ballCords[0] - closestDefender.pos[0], app.ballCords[1] - closestDefender.pos[1]
    defenseDistance = int(magnitude([dxDefense, dyDefense]))
    doesDefenseCatch = doesCatchBall(closestDefender, defenseDistance)
    doesOffenseCatch = doesCatchBall(app.targetReceiver, offenseDistance)
    if (not doesOffenseCatch and not doesDefenseCatch) or ballOutOfBounds(app):
        if app.down != 4:
            app.down += 1
            togglePlayEndScreen(app, f'Incomplete Pass To {app.targetReceiver.name}')
        else: 
            app.down = 1
            togglePlayEndScreen(app, f"Turnover on Downs")
            switchTeams(app, True)
      
    elif doesOffenseCatch and  not doesDefenseCatch:
        app.selectedPlayer = app.targetReceiver
        for player in app.playerList:
            player.accVector = [0,0]
        app.isRunning = True
        carrierStats = statsToAddTo(app, app.targetReceiver.key, app.teamOnOffense)
        carrierStats['Receptions'] += 1
        qbStats['Completions'] += 1
        app.ballInAir = False
    elif doesOffenseCatch and doesDefenseCatch:
        situation = random.randint(1,4)
        if situation == 1 or situation == 2:
            if app.down != 4:
                app.down += 1
                togglePlayEndScreen(app, f'Ball knocked down by {closestDefender.name}')
            else:
                app.down = 1
                togglePlayEndScreen(app, f"Turnover on Downs")
                switchTeams(app, True)
        elif situation == 3:
            app.ballCords = copy.copy(closestDefender.pos)
            app.ballVeloc = [0,0]
            app.ballAccVector = [0,0]
            if closestDefender.pos[0] > 50:
                app.lineOfScrimmage = closestDefender.pos[0]
            else:
                app.lineOfScrimmage = 220
            qbStats['INTs'] += 1
            togglePlayEndScreen(app, f"Intercepted by {closestDefender.name}")
            switchTeams(app, True)
        else: 
            app.ballInAir = False
            app.selectedPlayer = app.targetReceiver
            for player in app.playerList:
                player.accVector = [0,0]
            app.isRunning = True
            carrierStats = statsToAddTo(app, app.targetReceiver.key, app.teamOnOffense)
            carrierStats['Receptions'] += 1
            qbStats['Completions'] += 1
    else: #doesDefenseCatch and not doesOffenseCatch is only other possibility
        app.ballCords = copy.copy(closestDefender.pos)
        app.ballVeloc = [0,0]
        app.ballAccVector = [0,0]
        qbStats['INTs'] += 1
        if closestDefender.pos[0] > 50:
            app.lineOfScrimmage = closestDefender.pos[0]
        else:
            app.lineOfScrimmage = 220
        togglePlayEndScreen(app, f"Intercepted by {closestDefender.name}")
        switchTeams(app, True)



def doesCatchBall(receiver, distance):
    if distance > receiver.catchRadius:
        return False
    numerator = receiver.catchRadius - distance
    randomInt = random.randint(0, distance)
    return randomInt <= numerator

def endGame(app):
    app.gameOver = True
    app.isRunning = False
    app.isPaused = True
    app.isPassing = False
    changeRecords(app)
    loadRecords(app)

#Rewrites CSV records file
def changeRecords(app):
    lines = []
    #Used https://docs.python.org/3/library/datetime.html#date-objects to help with datetime and date
    currDate = date.today()
    #Use a list here instead of looping through the dictionary to maintain order
    recordList = ['Points', 'Passing TDs', 'Passing Yards', 'Completions', 'Attempts', 'Rushing Yards', 'Rushing Attempts', 
                  'Rushing TDs', 'INTs', 'Targets', 'Receptions', 'Receiving TDs', 'Receiving Yards']
    for record in recordList:
        isBroken = checkIfBroken(app, record)
        if isBroken[0]:
            player = isBroken[1]
            newRecord = str(isBroken[2])
            lines.append([record]+[player]+[newRecord]+[currDate])
        else:
            lines.append([record]+app.recordsDict[record])
    #Used https://www.youtube.com/watch?v=q5uM4VKywbA to help learn how to use CSV
    with open('gamerecords.csv', 'w', newline='') as csv_file:
        gameRecordsCSV = csv.writer(csv_file)
        gameRecordsCSV.writerow(['Record', 'Player', 'Value', 'Date'])
        for line in lines:
            gameRecordsCSV.writerow(line)

#Determines if a particular records was proken or not
def checkIfBroken(app, record):
    if len(app.recordsDict[record][1]) > 2 and app.recordsDict[record][1][-2] == '.':
        numberToBeat = int(float(app.recordsDict[record][1]))
    else:
        numberToBeat = int(app.recordsDict[record][1])
    originalValue = numberToBeat
    #Team Records
    if record == 'Points':
        teamWhoBeatIt = ''
        if app.team1Score > numberToBeat:
            numberToBeat = app.team1Score
            teamWhoBeatIt = app.teamList[app.selectedTeam1Index]
        if app.team2Score > numberToBeat:
            numberToBeat = app.team2Score
            teamWhoBeatIt = app.teamList[app.selectedTeam2Index]
        if originalValue == numberToBeat:
            return[False]
        else:
            return[True, teamWhoBeatIt, numberToBeat]
    #Checks QB Records
    elif record in {'Passing TDs', 'Passing Yards', 'Completions', 'Attempts', 'Rushing Yards', 'Rushing Attempts', 'Rushing TDs', 'INTs'}:
        teamWhoBeatIt = 0
        if app.qb1Stats[record] > numberToBeat:
            numberToBeat = app.qb1Stats[record] 
            teamWhoBeatIt = 1
        if app.qb2Stats[record] > numberToBeat:
            numberToBeat = app.qb2Stats[record]
            teamWhoBeatIt = 2
        if originalValue == numberToBeat:
            return[False]
        else:
            if teamWhoBeatIt == 1:
                index = app.selectedTeam1Index
            else:
                index = app.selectedTeam2Index
            team = app.teamList[index]
            player = app.teamRosters[team]['qb'].name
            return[True, player, int(numberToBeat)]
    #Checks receiver records
    else:
        statList = [app.team1WR1Stats, app.team2WR1Stats, app.team1WR2Stats, app.team2WR2Stats, app.team1TEStats, app.team2TEStats, app.team1RBStats, app.team2RBStats]
        for i in range(len(statList)):
            stats = statList[i]
            if stats[record] > numberToBeat:
                indexWhoBeat = i
                numberToBeat = stats[record]
        if originalValue == numberToBeat:
            return [False]
        else:
            key, team = getPlayerAndTeam(app, indexWhoBeat)
            if team == 1:
                teamIndex = app.selectedTeam1Index
            else: 
                teamIndex = app.selectedTeam2Index
            teamName = app.teamList[teamIndex]
            player = app.teamRosters[teamName][key].name
            return [True, player, int(numberToBeat)]

#Used to get player who beat repord
def getPlayerAndTeam(app, i):
    resultDict = {
        0: ('wr1', 1),
        1: ('wr1', 2),
        2: ('wr2', 1),
        3: ('wr2', 2),
        4: ('te', 1),
        5: ('te', 2),
        6: ('rb', 1),
        7: ('rb', 2)
    }
    return resultDict[i][0], resultDict[i][1], 


def togglePlayEndScreen(app, message):
    if app.nextQuarter and app.quarter == 4:
        endGame(app)
    else:
        if app.nextQuarter:
            endOfQuarter(app)
        app.betweenPlays = True
        app.isPaused = True
        app.message = message
        app.clockRunning = False
        app.catchable = False
        getInFormation(app)

def choosePlay(app):
    app.playChoiceScreen = True
    app.isPaused = True

def getNearestReceiver(app):
    closest = None
    closestDistance = 9999999
    for receiver in app.receiverList:
        dx = receiver.pos[0] - app.ballTarget[0]
        dy = receiver.pos[1] - app.ballTarget[1]
        distance = magnitude([dx,dy])
        if distance < closestDistance:
            closest = receiver
            closestDistance = distance
    return closest


#Used to determine physics variables for the ball
def getParabolaVars(distance, dx, dy):
    #acceleration is 2
    a = 2
    totalVelocity = math.sqrt(a*distance)
    velocityX = totalVelocity / math.sqrt(a)
    velocityY = totalVelocity / math.sqrt(a)
    magnitudeX = magnitude([dx, dy])
    unitVectorX = [dx/magnitudeX, dy/magnitudeX]
    velocityVectorX = [unitVectorX[0] * velocityX, unitVectorX[1] *velocityX]
    unitVectorY = [-1*dy/magnitudeX, dx/magnitudeX]
    velocityVectorY = [unitVectorY[0] * velocityY, unitVectorY[1] *velocityY]
    gVector = [2*unitVectorY[0]*-1, 2*unitVectorY[1]*-1]
    return velocityVectorX, velocityVectorY, gVector, velocityY



def findRandomPointInCircle(r):
    isNegative = 0
    xPoint = random.randint(-1*r, r)
    yPoint = random.randint(-1*r, r)
    if magnitude([xPoint, yPoint]) <= r:
        return xPoint, yPoint
    else:
        return findRandomPointInCircle(r)


def runPlay(app, play, routeIndex):
    app.selectedPlayer = app.qb
    app.clockRunning = True
    for receiver in app.receiverList:
        route = play[receiver.key][routeIndex]
        #Makes sure receiver does not go out
        if (receiver.pos[1] < 75 and route[1] < 0) or (receiver.pos[1] > 625 and route[1] > 1):
            route = (route[0], 0)
        goTowards(app, receiver, route)
    


def goTowards(app, player, point):
    dx = point[0]
    dy = point[1]
    if magnitude([dx,dy]) > 5:
        unitVector = [dx/(math.sqrt(dx**2+dy**2)), dy/(math.sqrt(dx**2+dy**2))]
        player.accVector = [unitVector[0] * math.sqrt(player.acc), unitVector[1] * math.sqrt(player.acc)]
    else:
        player.accVector=[0,0]
        player.veloc = [0,0]
        player.pos = [player.pos[0]+dx, player.pos[1]+dy]

def isBeingTackled(app):    
    closest, distance = closestDefenderAndDistance(app)
    if distance < 20:
        return [True, closest.name]
    else:
        return [False]

def closestDefenderAndDistance(app):
    closestDefender = None
    closestDistance = 999999999
    for defender in app.defenderList:
        dx = defender.pos[0] - app.selectedPlayer.pos[0]
        dy = defender.pos[1] - app.selectedPlayer.pos[1]
        distance = magnitude([dx, dy])
        if distance < closestDistance:
            closestDistance = distance
            closestDefender = defender
    return closestDefender, closestDistance

def isClose(v1, v2, epsilon):
    dx = v1[0] - v2[0]
    dy = v2[1] - v2[1]
    return magnitude([dx, dy]) <= epsilon

def adjustMagnitude(vector, scalar):
    if vector == [0,0]:
        return [0,0]
    norm = magnitude(vector)
    unitVector = [vector[0] / norm, vector[1] / norm]
    return [unitVector[0] * scalar, unitVector[1]* scalar]

def endOfQuarter(app):
    if app.quarter == 2:
        if app.teamOnOffense == 1:
            switchTeams(app, False)
        else:
            app.lineOfScrimmage = app.driveStartX
            app.toGo = 110
            app.down = 1

    app.quarter += 1
    app.timeToGo = app.quarterTime
    app.nextQuarter = False

def bounceBall(app, bouncability, friction, minBounce):
    app.ballCatchable = False
    oldVector = copy.copy(app.ballYVelocVector)
    app.ballYVelocVector = [bouncability*app.ballYVelocVector[0], bouncability*app.ballYVelocVector[1]]
    app.ballVeloc = [app.ballVeloc[0] + oldVector[0], app.ballVeloc[1] + oldVector[1]]
    retention = 1 - friction
    app.ballVeloc =  [app.ballVeloc[0] * retention, app.ballVeloc[1] * retention]
    app.ballVeloc = [app.ballVeloc[0] + app.ballYVelocVector[0], app.ballVeloc[1] + app.ballYVelocVector[1]]
    app.ballYVeloc *= (-1*bouncability)
    if magnitude(app.ballYVelocVector) < minBounce:
        stopBouncing(app)

def stopBouncing(app):
    app.bouncable = False
    app.ballVeloc = [0, 0]
    app.ballYVeloc = 0
    app.ballAccVector = [0, 0]
    app.ballHeight = 0
    app.ballAcc = 0
    app.isGoingDown = False
    app.ballInAir = False

def scoreSafety(app):
    if app.teamOnOffense == 1:
        app.team2Score += 2
    else:
        app.team1Score +=2

def updateTime(app):
    if app.timeToGo != 0:
        app.timeToGo -= 1
    else:
        app.nextQuarter = True

def updateBallPos(app):
    app.ballCords = [app.ballCords[0] + app.ballVeloc[0], app.ballCords[1]+app.ballVeloc[1]]
    app.ballVeloc = [app.ballVeloc[0]+app.ballAccVector[0], app.ballVeloc[1]+app.ballAccVector[1]]
    app.ballHeight += app.ballYVeloc
    app.ballYVeloc -= app.ballAcc  

def playersGoForBall(app):
    dx = app.ballTarget[0] - app.targetReceiver.pos[0]
    dy = app.ballTarget[1] - app.targetReceiver.pos[1]
    goTowards(app, app.targetReceiver, [dx, dy])
    for receiver in app.receiverList:
        if receiver != app.targetReceiver:
            receiver.accVector = [0,0]
        for defender in (app.defenderList[:app.selectedDefenderIndex]+app.defenderList[app.selectedDefenderIndex+1:]):
            if app.ballTarget != None:
                dx = app.ballTarget[0] - defender.pos[0]
                dy = app.ballTarget[1] - defender.pos[1]
                goTowards(app, defender, [dx, dy])
    if app.ballHeight <= 5 and app.isGoingDown == True and app.targetReceiver != None and app.catchable:
        catchBall(app)
    if app.isGoingDown == False and app.ballHeight >= 5:
        app.isGoingDown = True

def statsToAddTo(app, playerKey, team):
    playerKeyAndTeam = (playerKey, team)
    d = {
        ('wr1', 1): app.team1WR1Stats,
        ('wr1', 2): app.team2WR1Stats,
        ('wr2', 1): app.team1WR2Stats,
        ('wr2', 2): app.team2WR2Stats,
        ('te', 1): app.team1TEStats,
        ('te', 2): app.team2TEStats,
        ('rb', 1): app.team1RBStats,
        ('rb', 2): app.team2RBStats,
        ('qb', 1): app.qb1Stats,
        ('qb', 2): app.qb2Stats,
    }
    return d[playerKeyAndTeam]
def updateSpriteIndex(app):
    for player in app.playerList+app.defenderList:
        if almostEqual(player.veloc[0], 0):
            if player in app.defenderList:
                player.spriteIndex[1] = 1
            else:
                player.spriteIndex[1] = 0
        elif player.veloc[0] < 0:
            player.spriteIndex[1] = 0
        else:
            player.spriteIndex[1] = 1
        if player == app.qb:
            pass
        if magnitude(player.veloc) < 1:
            player.spriteIndex[0] = 0
        elif app.stepCounter % 5 == 0:
            if player.spriteIndex[0] == 0:
                player.spriteIndex[0] = 1
            else:
                player.spriteIndex[0] = 0


def onStep(app):
    #Used for animations
    app.stepCounter += 1
    #Bounces ball
    if app.ballHeight <= 0 and app.isGoingDown and app.bouncable:
        bounceBall(app, .3, .65, 1)
    #Updates time
    if app.clockRunning:
        updateTime(app)
    #Updates rush clock
    if app.isPassing:
        if app.rushClock > 0:
            app.rushClock -= 1
    #Makes sure that every defender and the target receiver goes towards the ball
    if app.ballInAir:
        updateBallPos(app)
        if not app.isPaused:
            playersGoForBall(app)
    
    if not app.isPaused:
        #Used for animations
        updateSpriteIndex(app)
        #Updates Physics variables for all the players
        for player in (app.playerList+app.defenderList):
            #Changes velocity according to acceleration but puts limit on velocity
            if magnitude(player.veloc) < player.speed:
                player.veloc[0] += player.accVector[0]
                player.veloc[1] += player.accVector[1]
            else:
                if adjustMagnitude(player.accVector, player.speed) != [0,0]:
                    player.veloc = adjustMagnitude(player.accVector, player.speed)

            #Controls the slowing down of the playters
            if player.accVector[0] and player.veloc[0] != 0 and player.accVector[0] / abs(player.accVector[0]) != player.veloc[0] / abs(player.veloc[0]):
                player.veloc[0] -= player.veloc[0] / 2
            if player.accVector[1] != 0 and player.veloc[1] != 0 and player.accVector[1] / abs(player.accVector[1]) != player.veloc[1] / abs(player.veloc[1]):
                player.veloc[1] -= player.veloc[1] / 2
            if player.accVector[0] == 0 and player.veloc[0] != 0:
                player.veloc[0] -= player.veloc[0]/2
            if player.accVector[1] == 0 and player.veloc[1] != 0:
                player.veloc[1] -= player.veloc[1]/2

            #Changes position according to velocity
            player.pos[0] += player.veloc[0]
            player.pos[1] += player.veloc[1]
            #Runs the play
            if app.isPassing:
                selectedDefender = app.defenderList[app.selectedDefenderIndex]
                runPlay(app, app.selectedPlay, app.routeIndex)
                dx = app.wr1.pos[0] - app.lastWR1Cords[0]
                dy = app.wr1.pos[1] - app.lastWR1Cords[1]
                if app.rushClock != 0 and app.qb.pos[0] <= app.lineOfScrimmage:
                    app.qb.pos[0] = app.lineOfScrimmage + 1
                    app.qb.veloc[0] = 0
                    app.qb.accVector[0] = 0
                #Makes sure they don't go past end zone
                for receiver in app.receiverList:
                    if receiver.pos[0] <= 10:
                        receiver.veloc[0] = 0
                        receiver.accVector[0] = 0
                #Makes sure the user cannot rush before the rush clock runs out
                if app.rushClock != 0 and selectedDefender.pos[0] >= app.lineOfScrimmage:
                    selectedDefender.pos[0] = app.lineOfScrimmage
                    selectedDefender.veloc[0] = 0
                    selectedDefender.accVector[0] = 0
                #Runs the players with new indexes, and also controls the movement of the receivers after play indexes run out
                if abs(dx) >= abs(app.selectedPlay['wr1'][app.routeIndex][0]) and abs(dy) >= abs(app.selectedPlay['wr1'][app.routeIndex][1]):
                    if app.routeIndex != len(app.selectedPlay['wr1']) - 1:
                        app.routeIndex += 1
                        app.lastWR1Cords = copy.copy(app.wr1.pos)
                    else:
                        for receiver in app.receiverList:
                            if receiver.pos[1] > 50 and receiver.pos[1] < 550 and receiver.veloc[0] < 0:
                                goTowards(app, receiver, receiver.veloc)
                            elif receiver.pos[1] <= 50 or receiver.pos[1] >= 550:
                                receiver.accVector[1] *= -.5
                                receiver.veloc[1] *= -1
                            if receiver.veloc[0] > 0:
                                receiver.veloc[0] = -1
                                receiver.accVector[0] = -.1
                #Allows for QB Scrambles
                if app.qb.pos[0] < app.lineOfScrimmage and app.rushClock == 0:
                    app.isPassing = False 
                    app.isRunning = True
                    for receiver in app.receiverList:
                        receiver.accVector = [0,0]
                        
                for defender in (app.defenderList[:app.selectedDefenderIndex]+app.defenderList[app.selectedDefenderIndex+1:]):
                    assignment = defender.assignment
                    #Controls the actions of the man-coverage defenders
                    if assignment != None and not (defender == app.spy and app.rushClock == 0):
                        horizontalDistance = abs(assignment.pos[0]-defender.pos[0])
                        if (assignment.pos[0]+25 > defender.pos[0]) and (defender.pos[0] == app.lineOfScrimmage - 100):
                            dx = 0
                            dy = assignment.pos[1]-defender.pos[1]
                            if dy != 0:
                                goTowards(app, defender, [dx, dy])
                        else:
                            dx = assignment.pos[0]-defender.pos[0]
                            dy = assignment.pos[1]-defender.pos[1]
                            goTowards(app, defender, [dx, dy])  
                    if defender.pos[1] <= 50 or defender.pos[1] >= 550:
                            defender.accVector[1] = 0
                            defender.veloc[1] = 0
                #Controls actions for rusher/spy
                if app.rushClock == 0 and selectedDefender != app.spy:
                    dx = app.qb.pos[0] - app.spy.pos[0]  
                    dy = app.qb.pos[1] - app.spy.pos[1]   
                    goTowards(app, app.spy, [dx, dy])
                #Plays defense for the safety
                if selectedDefender != app.safety:     
                    playSafetyDefense(app)
            #Moves ball with player
            if not app.ballInAir and app.selectedPlayer != None:
                app.ballCords = [app.selectedPlayer.pos[0], app.selectedPlayer.pos[1] + 5]
        if app.isRunning:
            #Has every defender go after ball carrier
            for defender in (app.defenderList[:app.selectedDefenderIndex]+app.defenderList[app.selectedDefenderIndex+1:]):
                dx = app.selectedPlayer.pos[0] - defender.pos[0]
                dy = app.selectedPlayer.pos[1] - defender.pos[1]
                goTowards(app, defender, [dx, dy])
        if app.isRunning or app.selectedPlayer == app.qb:
            if detectTouchdown(app):
                qbStats = statsToAddTo(app, 'qb', app.teamOnOffense)
                yards = (app.lineOfScrimmage // 11)
                if app.selectedPlayer == app.qb:
                    qbStats['Rushing TDs'] += 1
                    qbStats['Rushing Attempts'] += 1
                    qbStats['Rushing Yards'] += yards
                else:
                    carrierStats = statsToAddTo(app, app.selectedPlayer.key, app.teamOnOffense)
                    qbStats['Passing TDs'] += 1
                    qbStats['Passing Yards'] += yards
                    carrierStats["Receiving TDs"] += 1
                    carrierStats["Receiving Yards"] += yards
                if app.teamOnOffense == 1:
                    app.team1Score+=7
                else:
                    app.team2Score+=7
                togglePlayEndScreen(app, f"{app.selectedPlayer.name} scores a touchdown!")
                if not (app.quarter == 3 and app.timeToGo == app.quarterTime):
                    app.lineOfScrimmage = app.driveStartX
                    switchTeams(app, False)
            isTackled = isBeingTackled(app)
            if isTackled[0]:
                if app.selectedPlayer.pos[0] > 1150:
                    dx = app.lineOfScrimmage - 1150
                else:
                    dx = app.lineOfScrimmage-app.selectedPlayer.pos[0]
                if app.selectedPlayer == app.qb and dx < 0:
                    verb = 'sacked'
                else:
                    verb = 'tackled'
                app.lineOfScrimmage = app.selectedPlayer.pos[0]
                yards = int(dx/11)
                tackler = isTackled[1]
                qbStats = statsToAddTo(app, 'qb', app.teamOnOffense)
                if app.selectedPlayer == app.qb:
                    qbStats['Rushing Yards'] += yards
                    qbStats['Rushing Attempts'] += 1
                else:
                    qbStats['Passing Yards'] += yards
                    carrier = app.selectedPlayer.key
                    carrierStats = statsToAddTo(app, carrier, app.teamOnOffense)
                    carrierStats['Receiving Yards'] += yards
                if app.selectedPlayer.pos[0] > 1150:
                    scoreSafety(app)
                    togglePlayEndScreen(app, f"Safety")
                    switchTeams(app, False)
                elif dx >= app.toGo:
                    app.down = 1
                    app.toGo = 110
                    togglePlayEndScreen(app, f"{app.selectedPlayer.name} {verb} by {tackler}")
                elif app.down == 4:
                    togglePlayEndScreen(app, f"Turnover on Downs")
                    switchTeams(app, True)
                else:
                    app.down += 1
                    app.toGo -= dx
                    togglePlayEndScreen(app, f"{app.selectedPlayer.name} {verb} by {tackler}")
            if app.selectedPlayer != None and (app.selectedPlayer.pos[1] > 550 or app.selectedPlayer.pos[1] < 50):
                if app.selectedPlayer.pos[0] < 1150:
                    dx = app.lineOfScrimmage-app.selectedPlayer.pos[0]
                else:
                    dx = app.lineOfScrimmage
                yards = int(dx/11)
                app.lineOfScrimmage = app.selectedPlayer.pos[0]
                qbStats = statsToAddTo(app, 'qb', app.teamOnOffense)
                
                if app.selectedPlayer == app.qb:
                    qbStats['Rushing Yards'] += yards
                    qbStats['Rushing Attempts'] += 1
                else:
                    receiverStats = statsToAddTo(app, app.selectedPlayer.key, app.teamOnOffense)
                    qbStats['Passing Yards'] += yards
                    receiverStats['Receiving Yards'] += yards
                if app.selectedPlayer.pos[0] > 1150:
                    scoreSafety(app)
                    togglePlayEndScreen(app, f"Safety")
                    switchTeams(app, False)
                elif dx >= app.toGo:
                    app.down = 1
                    app.toGo = 110
                    togglePlayEndScreen(app, f"First Down")
                elif app.down == 4:
                    togglePlayEndScreen(app, f"Turnover on Downs")
                else:
                    app.down += 1
                    app.toGo -= dx
                    togglePlayEndScreen(app, f"{app.selectedPlayer.name} out of bounds for {yards} yards")

def furthestReceiver(receiverList):
    furthest = None
    for receiver in receiverList:
        xPos = receiver.pos[0]
        if furthest == None or xPos < furthest:
            furthest = xPos
    return furthest

def playSafetyDefense(app):
    #Checks how many receivers have past original starting spot
    receiversToGuard = getReceiversToGuard(app)
    if receiversToGuard == []:
        optimalSpot = optimizeSafety1d(app)
        dy = optimalSpot-app.safety.pos[1]
        goTowards(app, app.safety, [0, dy])
    elif furthestReceiver(receiversToGuard) > (app.lineOfScrimmage//2)-50:
        optimalSpot = optimizeSafety1d(app)
        dy = optimalSpot-app.safety.pos[1]
        goTowards(app, app.safety, [-50, dy])
    else:
        optimalSpot = optimizeSafety2d(app, receiversToGuard)
        dx = optimalSpot[0]-app.safety.pos[0]
        dy = optimalSpot[1]-app.safety.pos[1]
        goTowards(app, app.safety, [dx-50, dy])

def optimizeSafety2d(app, receiverList):
    optimalSpot = None
    shortestTotalDistance = None
    potentialSpots = generatePotentialSpots(app)
    for potentialSpot in potentialSpots:
        totalDistance = distancesSquared(potentialSpot, receiverList, app)
        if shortestTotalDistance == None or totalDistance < shortestTotalDistance:
            shortestTotalDistance = totalDistance
            optimalSpot = potentialSpot
    return optimalSpot

def generatePotentialSpots(app):
    potentialSpots = []
    minX = None
    for receiver in app.receiverList:
        if minX == None or receiver.pos[0] < minX:
            minX = receiver.pos[0]
    minX = int(minX)
    maxX = int((app.lineOfScrimmage)//2)
    for x in range(minX, maxX, 50):
        for y in range(50, 551, 50):
            potentialSpots.append([x, y])
    return potentialSpots


def optimizeSafety1d(app):
    optimalSpot = None
    shortestTotalDistance = None
    potentialSpots = list(range(50, 551, 25))
    listToUse = copy.copy(app.receiverList)
    if app.rb.pos[0] > app.lineOfScrimmage:
        listToUse.remove(app.rb)
    for potentialSpot in potentialSpots:
        totalDistance = distancesSquared([app.safety.pos[0], potentialSpot], listToUse, app)
        if shortestTotalDistance == None or totalDistance < shortestTotalDistance:
            optimalSpot = potentialSpot
            shortestTotalDistance = totalDistance
    return optimalSpot

def distancesSquared(spot, receiverList, app):
    sum = 0
    mostOpen = biggestSeperation(app, receiverList)
    for receiver in receiverList:
        dx = spot[0]-receiver.pos[0]
        dy = spot[1]-receiver.pos[1]
        seperation = getSeperation(receiver, app)
        adjustment = seperation/mostOpen
        adjustment *= adjustment
        #Squares the adjustment to increase the weight of it
        dx *= adjustment
        dy *= adjustment
        distanceSquared = magnitude([dx, dy])**2
        sum += distanceSquared
    return sum

def getSeperation(receiver, app):
    for defender in app.defenderList:
        if defender.assignment == receiver:
            assignedDefender = defender
    dx = receiver.pos[0]-assignedDefender.pos[0]
    dy = receiver.pos[1]-assignedDefender.pos[1]
    return magnitude([dx, dy])

def biggestSeperation(app, receiverList):
    biggest = None
    for defender in app.defenderList:
        if defender.assignment != None:
            assignment = defender.assignment
            #Note that I did not use the above function due to efficiency for this purpose
            dx = assignment.pos[0] - defender.pos[0]
            dy = assignment.pos[1] - defender.pos[1]
            seperation = magnitude([dx, dy])
            if biggest == None or seperation > biggest:
                biggest = seperation
    return biggest

def getReceiversToGuard(app):
    result = []
    for receiver in app.receiverList:
        if receiver.pos[0] < ((app.lineOfScrimmage)//2):
            result.append(receiver)
    return result


def detectTouchdown(app):
    xCord = app.selectedPlayer.pos[0]
    if xCord < 50:
        return True
    else:
        return False       

def magnitude(v):
    return math.sqrt(v[0]**2 + v[1]**2)

def getInFormation(app):
    app.rushClock = 75
    app.ballHeight = 0
    app.isRunning = False
    for player in app.playerList+app.defenderList:
        player.veloc = [0, 0]
        player.accVector = [0,0]
    app.ballCord = [-100, -100]
    app.wr1.pos = [app.lineOfScrimmage, 500]
    app.wr2.pos = [app.lineOfScrimmage+20, 70]
    app.te.pos = [app.lineOfScrimmage, 200]
    app.rb.pos = [app.lineOfScrimmage+170, 300]
    app.qb.pos = [app.lineOfScrimmage+20, 300]
    #app.ballCords = copy.copy(app.qb.pos)
    app.targetReceiver = None
    app.defender1.pos = [app.lineOfScrimmage-100, 500]
    app.defender2.pos = [app.lineOfScrimmage-100, 70]
    app.defender3.pos = [app.lineOfScrimmage-100, 200]
    app.defender4.pos = [app.lineOfScrimmage-100, 325]
    app.spy.pos = [app.lineOfScrimmage-100, 275]
    app.safety.pos = [(app.lineOfScrimmage)//2, 300]
    app.routeIndex = None
    app.lastWR1Cords = None
    app.isPassing = False
    app.isRunning = False
    app.targetCords = None
    app.ballTarget = [-300, -300]
    app.targetReceiver = app.wr1

def main():
    runApp()

main()
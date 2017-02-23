###########################################################
# GLOBALS -- change to modify script behavior
# Initial ELO for all new teams
gInitialELO = 1500
# Regular Season K value
gRegularSeasonK = 20
# Path to team file
gTeamFile = "data/teams.txt"
# Path to root of matches directory
gMatchPath = "data/matches/"
# END GLOBALS
###########################################################

import csv, os
from enum import Enum

#class Region(Enum):
#	NA = 1 # North America
#	EU = 2 # Europe
#	KR = 3 # Korea
#	CN = 4 # China
#	LA = 5 # Latin America
#	AZ = 6 # Australia/New Zealand
#	SA = 7 # Southeast Asia
#	TW = 8 # Taiwan

#gRegionNames = {
#	"NA":Region.NA,
#	"EU":Region.EU,
#	"KR":Region.KR,
#	"CN":Region.CN,
#	"LA":Region.LA,
#	"AZ":Region.AZ,
#	"SA":Region.SA,
#	"TW":Region.TW
#}

class Team:
	def __init__(self):
		self.mName = ""
		self.mRegion = ""
		self.mELO = gInitialELO
		self.mWins = 0
		self.mLosses = 0
		self.mGameWins = 0
		self.mGameLosses = 0

gTeamDict = {}

def loadTeams(file):
	with open(file, newline='') as f:
		reader = csv.reader(f)
		for row in reader:
			team = Team()
			team.mName = row[0]
			team.mRegion = row[1]
			gTeamDict[team.mName] = team
	#for k in gTeamDict:
	#	print(k,":",vars(gTeamDict[k]))

def computeWinE(teamAELO,teamBELO):
	return 1 / (pow(10, -(teamAELO-teamBELO)/400) + 1)

def computeMatch(data):
	if not (data[0] in gTeamDict):
		print("ERROR: Team",data[0],"not found!")
		return
	if not (data[1] in gTeamDict):
		print("ERROR: Team",data[1],"not found!")
		return
		
	teamA = gTeamDict[data[0]]
	teamB = gTeamDict[data[1]]
	teamAWins = int(data[2])
	teamBWins = int(data[3])
	
	teamAWinE = computeWinE(teamA.mELO, teamB.mELO)
	teamBWinE = 1 - teamAWinE
	print("{0} ({1}%) vs {2} ({3}%)".format(teamA.mName, 
		teamAWinE * 100, teamB.mName, teamBWinE * 100))
	
	# Update win/losses
	teamA.mGameWins += teamAWins
	teamA.mGameLosses += teamBWins
	teamB.mGameWins += teamBWins
	teamB.mGameLosses += teamAWins
	
	if teamAWins > teamBWins:
		teamA.mWins += 1
		teamB.mLosses += 1
	else:
		teamA.mLosses += 1
		teamB.mWins += 1
		
def computeMatches(rootDir):
	files = os.listdir(rootDir)
	files.sort() # Sort this just in case
	for fileName in files:
		print(fileName)
		with open(gMatchPath + fileName, newline='') as f:
			reader = csv.reader(f)
			for row in reader:
				#print(row)
				computeMatch(row)
	
def main():
	loadTeams(gTeamFile)
	computeMatches(gMatchPath)
	for k in gTeamDict:
		print(k,":",vars(gTeamDict[k]))

if __name__ == "__main__":
	main()
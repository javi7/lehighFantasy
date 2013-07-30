from bs4 import BeautifulSoup
from optparse import OptionParser
import requests 
import re
import sys
from sqlalchemy import *
execfile('teamMap.py')

parser = OptionParser()
parser.add_option('-y', '--year', dest='year', default='2012',
	help='enter year to scrape stats for')
parser.add_option('-l', '--league', dest='league', default='36878',
	help='enter league to scrape stats for')
parser.add_option('-w', '--week', dest='week',
	help='enter week to scrape stats for')
(options, args) = parser.parse_args()

performanceFields = ['playerId', 'gameId', 'franchiseId', 'points', 'nflTeam',
'ir', 'byeWeek', 'starter', 'passYds', 'passTDs', 'passInt', 'rushYds', 'rushTDs', 'recYds',
'recTDs', '2pc', 'fumL', 'miscTDs', 'madeFG39', 'attFG39', 'madeFG49', 'attFG49', 'madeFG50', 'attFG50',
'madeXP', 'attXP', 'defTDs', 'defInt', 'defFumR', 'sacks', 'safeties', 'blocks', 'pointsAllowed', 'totalPts', 'slot'] 
positionPlayerStats = ['passYds', 'passTDs', 'passInt', 'rushYds', 'rushTDs', 'recYds', 'recTDs', '2pc', 'fumL', 'miscTDs', 'totalPts']
kickerStats = ['madeFG39', 'attFG39', 'madeFG49', 'attFG49', 'madeFG50', 'attFG50','madeXP', 'attXP', 'totalPts']
defenseStats = ['defTDs', 'defInt', 'defFumR', 'sacks', 'safeties', 'blocks', 'pointsAllowed', 'totalPts']


playerFields = ['id', 'name', 'position']
 
db = create_engine("mysql://javi:cs3200@localhost/LehighFantasy").connect()

yearQueryResult = 0

try:
    yearSelect = 'SELECT id FROM Season WHERE year=' + str(options.year)
    print 'executing ' + yearSelect
    yearQueryResult = db.execute(yearSelect).first()[0]
    insert = 'INSERT INTO Week (weekNumber, seasonId) VALUES (' + str(options.week) + ', ' + str(yearQueryResult) + ')'
    print 'executing ' + insert
    db.execute(insert)
    print 'inserted week ' + str(options.week)
except:
    print 'inserting week # ' + str(options.week) + ' failed'
    sys.exit('week might already exist in database')

try:
	select = 'SELECT id FROM Week WHERE seasonId=' + str(yearQueryResult) + ' AND weekNumber=' + str(options.week)
	print 'executing ' + select 
	weekQuery = db.execute(select)
	if weekQuery.rowcount == 1:
		weekId = weekQuery.first()[0]
	print 'week id is ' + str(weekId)
except:
	print 'week not found in db'
	sys.exit('select statement failed')

for x in range(12):
    url = 'http://games.espn.go.com/ffl/boxscorefull?leagueId=' + options.league + '&teamId=' + str(x + 1) + '&scoringPeriodId=' + options.week + '&seasonId=' + options.year + '&view=scoringperiod&version=full'
    print 'using url ' + url
    html = requests.get(url)
    soup = BeautifulSoup(html.text)
	
    teamInfos = soup.find('div', id = 'teamInfos')
    teamIdRegEx = re.compile('.*teamId.*')
    playerInfoRegEx = '.*, ([A-Za-z]{2,3})[\s|\xc2\xa0](QB|RB,WR|RB|WR|TE|K)[\xc2\xa0]*(P|Q|D|IR|O)?'	
    gameTeams = []
    for link in teamInfos.findAll('a'):
        if teamIdRegEx.match(link['href']):
            equals = link['href'].find('=', -4)
            gameTeams.append( int( link['href'][equals + 1:] ) )
    if options.year == '2011' and len(gameTeams) == 1:
        print gameTeams[0]
        gameTeams.append(1)
    print str( gameTeams[0] ) + ' vs ' + str( gameTeams[1] )
	
    gameSelect = 'SELECT * FROM Matchup m, Game g, Week w WHERE w.id=' + str(weekId) + ' AND w.id=g.weekId AND (m.franchiseId=' + str(gameTeams[0]) + ' OR m.franchiseId=' + str(gameTeams[1]) + ') AND m.gameId=g.id'
    print 'executing ' + gameSelect
    try:
        gameQuery = db.execute(gameSelect)
    except:
        print 'query for game failed'
        sys.exit('game select failed')

    if gameQuery.rowcount == 0:
        gameInsert = 'INSERT INTO Game (weekId) VALUES (' + str(weekId) + ')'
        print 'executing ' + gameInsert
        try:
            db.execute(gameInsert)
            
        except:
            print 'insertion of game failed'
            sys.exit('game insert failed')
        gameSelect = 'SELECT id FROM Game WHERE weekId=' + str(weekId) + ' ORDER BY ID DESC'
        print 'executing ' + gameSelect
        try:
            gameIdQuery = db.execute(gameSelect)
        except:
            print 'looking for game id failed'
            sys.exit('failed while looking for game id')
        gameId = gameIdQuery.first()[0]
        
        for team in gameTeams:
            matchupInsert = 'INSERT INTO Matchup VALUES(' + str(gameId) + ',' + str(team) + ')'
            print 'executing ' +  matchupInsert
            try:
                db.execute(matchupInsert)
            except:
                print 'matchup insert failed'
                sys.exit('failed while inserting matchup')
    else:
        print 'matchup already logged'
        continue 	

    print 'matchup not yet logged'

    playerRows = soup.findAll('tr', attrs={'class': 'pncPlayerRow'})
    franchiseId = str( gameTeams[0] )
    teamOneProcessed = False
    for row in playerRows:
        if row.find('td', attrs={'class': 'playerSlot'}).text == 'QB':
            if teamOneProcessed:
                franchiseId = str( gameTeams[1] )
            else:
                teamOneProcessed = True
        player = dict( (field, "NULL") for field in playerFields )
        performance = dict( (field, "NULL") for field in performanceFields )
        performance['franchiseId'] = franchiseId
        performance['gameId'] = gameId

        playerCell = row.find('td', attrs={'class': 'playertablePlayerName'})
        playerLink = row.find('a', attrs={'class': 'flexpop'})
        if not playerLink:
            continue
        playerSlot = row.find('td', attrs={'class': 'playerSlot'})	

        playerId = playerLink['playerid']
        performance['playerId'] = playerId
        player['id'] = playerId
        player['name'] = playerLink.text

        performance['slot'] = playerSlot.text
        if playerSlot.text == 'IR':
            performance['ir'] = '1'
            performance['starter'] = '0'
        else:
            if playerSlot.text == 'Bench':
                performance['starter'] = '0'
            else:
                performance['starter'] = '1'
            performance['ir'] = '0'

        playerString = playerCell.text
        info = re.match(playerInfoRegEx, playerString, re.S)
        if info:
            performance['nflTeam'] = info.group(1)
            player['position'] = info.group(2)
        else:
            teamName = playerLink.text[0:-5]
            player['position'] = 'D/ST'
            performance['nflTeam'] = teamMap[teamName]
        playerStats = row.findAll('td', attrs={'class': 'playertableStat'})
        statsDict = {}
        parsedStats = []
        
        if '--' in str(row):
            performance['byeWeek'] = '1'
            performance['totalPts'] = '0'
        else:
            performance['byeWeek'] = '0'
            if player['position'] == 'K':
                statCount = 1
                for stat in playerStats:
                    print str(statCount) + ' -- ' + stat.text
                    if statCount == 6:
                        parsedStats.append(stat.text)
                    elif statCount != 4:
                        fgStat = (stat.text).split('/')
                        for number in fgStat:
                            parsedStats.append(number)
                    statCount += 1
                statsDict = dict( zip( kickerStats, parsedStats ) )
            elif player['position'] == 'D/ST':
                for stat in playerStats:
                    parsedStats.append(stat.text)
                statsDict = dict( zip( defenseStats, parsedStats ) )
            else:
                statCount = 1
                for stat in playerStats:
                    if statCount != 1 and statCount != 5 and statCount != 8:
                        parsedStats.append(stat.text)
                    statCount += 1
                statsDict = dict( zip( positionPlayerStats, parsedStats ) )
            
            for key in statsDict.keys():
                performance[key] = statsDict[key]

        insertPlayerFields = ""
        insertPlayerValues = ""
        for key in player.keys():
            insertPlayerFields += key + ','
            insertPlayerValues += "'" + player[key] + "',"
        playerInsert = 'INSERT INTO Player (' + insertPlayerFields[0:-1] + ') VALUES (' + insertPlayerValues[0:-1] +')'
        print 'executing ' + playerInsert

        try:
            db.execute(playerInsert)
            print 'NEW PLAYER ADDED -- ' + player['name']
        except:
            print 'REPEAT VALUE -- Player already exists'

        insertPerformanceFields = ""
        insertPerformanceValues = ""
        for key in performance.keys():
            insertPerformanceFields += key +','
            insertPerformanceValues += "'" + str(performance[key]) + "',"
        performanceInsert = 'INSERT INTO Performance (' + insertPerformanceFields[0:-1] + ') VALUES (' + insertPerformanceValues[0:-1] + ')'
        print 'executing ' + performanceInsert

        try:
            db.execute(performanceInsert)
        except:
            print 'FAILED on performance insert'
            sys.exit('performance insert failed')	
        print ' '
        for key in player.keys():
            print key + ': ' + player[key]
        for key in performance.keys():
            print key + ': ' + str( performance[key] )
db.close()

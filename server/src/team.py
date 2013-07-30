class team:
    def GET(self, teamId):
        db = create_engine("mysql://javi:cs3200@localhost/LehighFantasy").connect()

        gamesDict = {}
        resultsList = []

        gameScoresSelect = "SELECT CONCAT_WS(' ', f.ownerFirstName, f.ownerLastName), SUM(p.totalPts), f.id, w.weekNumber, s.year, g.id FROM Franchise f, Performance p, Week w, Season s, Game g, Matchup m WHERE p.franchiseId=f.id AND p.gameId=g.id AND g.weekId = w.id AND w.seasonId = s.id AND p.starter=1 AND g.id=m.gameId AND m.franchiseId=" + str(teamId) + " GROUP BY p.gameId, p.franchiseId ORDER BY w.weekNumber"

        try:
            gameScoresResult = db.execute(gameScoresSelect)
            db.close()
        except:
            print gameScoresSelect + 'failed'
            return DB_ERROR 
            db.close()

        if gameScoresResult.rowcount == 0:
            return 'Invalid Team Id'
            
        for result in gameScoresResult:
            if result[5] in gamesDict.keys():
                gamesDict[ result[5] ].append(result)
            else:
                gamesDict[ result[5] ] = [result]
               
        teamOwner = ""

        for game in gamesDict.values():
            matchupDict = {}
            index = 0
            for scores in game:
                if int( scores[2] ) == int(teamId):
                    if teamOwner == "":
                        teamOwner = scores[0]
                    matchupDict['score'] = scores[1]
                    matchupDict['oppScore'] = game[1 - index][1]
                    matchupDict['week'] = scores[3]
                    matchupDict['opponent'] = game[1 - index][0]
                    matchupDict['opponentId'] = game[1 - index][2]
                    matchupDict['gameId'] = scores[5]
                    if len(resultsList) == 0:
                        resultsList.append(matchupDict)
                    else:
                        entryIndex = 0
                        for result in resultsList:
                            if matchupDict['week'] < result['week']:
                                break
                            entryIndex += 1
                        resultsList.insert(entryIndex, matchupDict)

                index += 1 

        gameList = HTML_HEADER
        gameList += "<h1>" + teamOwner + '</h1><table class="table table-hover"><thead><tr><th>Week</th><th>Opponent</th><th>Result</th></tr></thead><tbody>'
        for result in resultsList:
            gameList += '<tr><td>' + str( result['week'] ) + '</td>'
            gameList += '<td><a href="/team/' + str( result['opponentId'] ) + '">' + result['opponent'] + '</a></td>'
            gameResult = ""
            if result['score'] > result['oppScore']:
                gameResult = "W"
            elif result['score'] < result['oppScore']:
                gameResult = "L"
            else:
                gameResult = "T"
            gameList += '<td><a href="/game/' + str( result['gameId'] ) + '">' + gameResult + ' ' + str( result['score'] ) + ' - ' + str( result['oppScore'] ) + ' </a></td></tr>'
            
        gameList += '</tbody></table>'
        gameList += HTML_FOOTER 
         
        return gameList

class standings:
    def GET(self):    
        db = create_engine("mysql://javi:cs3200@localhost/LehighFantasy").connect()

        gamesDict = {}
        standingsDict = {}
        sortedStandings = []

        gameScoresSelect = 'SELECT CONCAT_WS( \' \', f.ownerFirstName, f.ownerLastName ), SUM(p.totalPts), f.id, g.id FROM Franchise f, Performance p, Game g WHERE p.gameId=g.id AND p.franchiseId=f.id AND p.starter=1 GROUP BY p.gameId, p.franchiseId'

        try:
            gameScoresResult = db.execute(gameScoresSelect)
            db.close()
        except:
            print gameScoresSelect + 'failed'
            db.close()
            return DB_ERROR

        for result in gameScoresResult:
            if result[3] in gamesDict.keys():
                gamesDict[ result[3] ].append( result[:-1] )
            else:
                gamesDict[ result[3] ] = [ result[:-1] ]

        for game in gamesDict.values():
            points = [0, 0]
            points[0] = game[0][1]
            points[1] = game[1][1]
            index = 0
            for team in game:
                win = 0
                tie = 0
                loss = 0
                if points[index] > points[1 - index]:
                    win = 1
                elif points[index] < points[1 - index]:
                    loss = 1
                else:
                    tie = 1
                if team[0] in standingsDict.keys():
                    standingsDict[ team[0] ]['wins'] += win
                    standingsDict[ team[0] ]['losses'] += loss
                    standingsDict[ team[0] ]['ties'] += tie
                    standingsDict[ team[0] ]['pointsFor'] += points[index]
                    standingsDict[ team[0] ]['pointsAgainst'] += points[1 -index]
                    standingsDict[ team[0] ]['rankingPts'] += 2 * win + tie
                else:
                    standingsDict[ team[0] ] = { 'wins': win, 'losses': loss, 'ties': tie, 'pointsFor': points[index], 'pointsAgainst': points[1 - index], 'rankingPts': (2 * win + tie), 'id': team[2] }
                index += 1

        for name in standingsDict.keys():
            teamDict = { 'name': name }
            for key in standingsDict[name].keys():
                teamDict[key] = standingsDict[name][key]
            
            if len(sortedStandings) == 0:
                sortedStandings.append(teamDict)
            else:
                index = 0
                for index in range( len(sortedStandings) ):
                    compare = sortedStandings[index]
                    if teamDict['rankingPts'] > compare['rankingPts']:
                        break
                    elif teamDict['rankingPts'] == compare['rankingPts']:
                        if teamDict['wins'] > compare['wins']:
                            break
                        elif teamDict['wins'] == compare['wins']:
                            if teamDict['pointsFor'] > compare['pointsFor']:
                                break
                            elif teamDict['pointsFor'] == compare['pointsFor']:
                                if teamDict['pointsAgainst'] < compare['pointsAgainst']:
                                    break
                sortedStandings.insert(index, teamDict)
   
        standings = HTML_HEADER
        standings += '<table class="table table-hover"><thead><tr><th>Name</th><th>Wins</th><th>Losses</th><th>Ties</th><th>Points For</th><th>Points Against</th></tr></thead><tbody>'
        for entry in sortedStandings:
            standings += "<tr>"
            standings += '<td><a href="/team/' + str( entry['id'] ) + '">' + str( entry['name'] ) + "</a></td>"
            standings += "<td>" + str( entry['wins'] ) + "</td>"
            standings += "<td>" + str( entry['losses'] ) + "</td>"
            standings += "<td>" + str( entry['ties'] ) + "</td>"
            standings += "<td>" + str( entry['pointsFor'] ) + "</td>"
            standings += "<td>" + str( entry['pointsAgainst'] ) + "</td>"
            standings += "</tr>"
        standings += "</tbody></table>"
        standings += HTML_FOOTER
        db.close()
        return standings

class game:
    def GET(self, gameId):

            def printPlayerRow( player ) :
                playerPosition = player['slot']
                if player['slot'] == 'Bench' or player['slot'] == 'IR':
                    playerPosition = player['position']
                playerRow = '<tr><td>' + playerPosition + '</td>'
                playerRow += '<td>' + player['name'] + '</td>'
                playerRow += '<td><a href="/performance/' + str( player['id'] ) + '">' + str( player['points'] ) + '</a></td>'
                playerRow += '</tr>'
                return playerRow
        
            db = create_engine("mysql://javi:cs3200@localhost/LehighFantasy").connect()

            positionsList = ['QB', 'RB', 'RB/WR', 'WR', 'TE', 'K', 'D/ST']
            teamsDict ={}

            gameSelect = 'SELECT p.slot, p.totalPts, pl.name, p.franchiseId, CONCAT_WS(\' \', f.ownerFirstName, f.ownerLastName), pl.position, p.perfId FROM Franchise f, Performance p, Player pl WHERE p.franchiseId=f.id AND p.playerId=pl.id AND p.gameId=' + str(gameId)

            try:
                gameResults = db.execute(gameSelect)
                db.close()
            except:
                print gameSelect + ' failed'
                db.close()
                return DB_ERROR

            if gameResults.rowcount == 0:
                print 'invalid game id'
                sys.exit(0)

            for score in gameResults:
                if score[3] not in teamsDict.keys():
                    teamsDict[ score[3] ] = {}
                    teamsDict[ score[3] ]['owner'] = score[4]
                    
                if score[0] not in teamsDict[ score[3] ].keys():
                    teamsDict[ score[3] ][ score[0] ] = []
                teamsDict[ score[3] ][ score[0] ].append( { 'name': score[2], 'points': score[1], 'position': score[5], 'slot': score[0], 'id': score[6] } ) 

            gamePage = HTML_HEADER
            gamePage += '<div class="row">'
            
            for team in teamsDict.keys():
                gamePage += '<div class="span6">'
                gamePage += '<h2><a href="/team/' + str(team) + '">' + teamsDict[team]['owner'] + '</a></h2>'
               
                totalPts = 0 
                gamePage += '<h3>Starters</h3><table class="table table-hover"><tbody>'
                for position in positionsList:
                    for player in teamsDict[team][position]:
                        gamePage += printPlayerRow(player)
                        totalPts += player['points']
                gamePage += '<tr><td colspan="2">TOTAL</td><td>' + str(totalPts) + '</td></tr>'
                gamePage += '</tbody></table>'
                
                totalPts = 0
                gamePage += '<h3>Bench</h3><table class="table table-hover"><tbody>'
                for player in teamsDict[team]['Bench']:
                    gamePage += printPlayerRow(player)
                    totalPts += player['points']
                gamePage += '<tr><td colspan="2">TOTAL</td><td>' + str(totalPts) + '</td></tr>'
                gamePage += '</tbody></table>'
                
                if "IR" in teamsDict[team].keys():
                    gamePage += '<h3>Injured Reserve</h3><table class="table table-hover"><tbody>'
                    for player in teamsDict[team]['IR']:
                        gamePage += printPlayerRow(player)
                    gamePage += '</tbody></table>'
                
                gamePage += '</div>'
            
            gamePage += '</div>' + HTML_FOOTER            
            return gamePage

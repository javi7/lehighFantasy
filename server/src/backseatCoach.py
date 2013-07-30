import json
import pprint

class backseatCoach:
    def GET( self, teamId, gameId ):
        db = create_engine("mysql://javi:cs3200@localhost/LehighFantasy").connect()

        gameSelect = "SELECT p.totalPts, p.starter, p.slot, pl.position FROM Performance p, Player pl WHERE p.gameId=" + gameId + " AND p.franchiseId=" + teamId + " AND pl.id=p.playerId"

        try:
            gamePerformances = db.execute( gameSelect )
            db.close()
        except:
            print gameSelect + ' failed'
            db.close
            return DB_ERROR

        lineupMistakes = 0;
        actualScore = 0;
        perfectScore = 0;
        perfectLineup = {};
        bestRBs = [];
        bestWRs = [];
        flexMess = { "RB": bestRBs, "WR": bestWRs }
        debug = ""

        for performance in gamePerformances:
            if performance['slot'] in positionsList:
                actualScore += performance['totalPts']

            playerPosition = performance['position']
            notLast = False

            if playerPosition == 'RB' or playerPosition == 'WR':
                insertionIndex = 0
                for index in range( len( flexMess[playerPosition] ) ):
                    insertionIndex = index
                    if performance['totalPts'] > flexMess[playerPosition][index]['totalPts'] or ( performance['totalPts'] == flexMess[playerPosition][index]['totalPts'] and performance['starter'] == 1 ):
                        notLast = True
                        break     
                if not notLast:
                    insertionIndex += 1
                debug += playerPosition + str( performance['totalPts'] ) + '--' + str( insertionIndex ) + "\n"
                flexMess[playerPosition].insert(insertionIndex, performance)
            else:
                if playerPosition in perfectLineup.keys():
                    if performance['totalPts'] > perfectLineup[playerPosition][0]['totalPts'] or ( performance['totalPts'] == perfectLineup[playerPosition][0]['totalPts'] and performance['starter'] == 1 ):
                        perfectLineup[ playerPosition ] = [ performance ] 
            
                else:
                    perfectLineup[ playerPosition ] = [ performance ] 
        
        for pos in flexMess.keys():
            perfectLineup[pos] = []
            for index in range(2):
                perfectLineup[pos].append(flexMess[pos][index])
        
        if flexMess['RB'][2]['totalPts'] > flexMess['WR'][2]['totalPts'] or ( flexMess['RB'][2]['totalPts'] == flexMess['WR'][2]['totalPts'] and flexMess['RB'][2]['starter'] == 1 ):
            perfectLineup['RB/WR'] = [ flexMess['RB'][2] ]
        else:
            perfectLineup['RB/WR'] = [flexMess['WR'][2] ]

        for posList in perfectLineup.values():
            for player in posList:
                debug += player['position'] + ' -- ' + str( player['totalPts'] ) + "\n"
                perfectScore += player['totalPts']
                if player['starter'] == 0:
                    lineupMistakes += 1
                        
        result = { 'mistakes' : lineupMistakes, 'actualPts': actualScore, 'possiblePts': perfectScore }
        
        pp = pprint.PrettyPrinter(indent=4)
        return pp.pformat(flexMess) + debug + json.dumps(result)

class performance:
    def GET(self, performanceId):
        db = create_engine("mysql://javi:cs3200@localhost/LehighFantasy").connect()
        
        performanceSelect = "SELECT p.*, pl.*, w.weekNumber, s.year, CONCAT_WS(' ', f.ownerFirstName, f.ownerLastName) AS ownerName FROM Performance p, Player pl, Franchise f, Week w, Season s, Game g WHERE p.perfId=" + str(performanceId) + " AND p.playerId = pl.id AND p.gameId=g.id AND g.weekId = w.id AND p.franchiseId=f.id AND w.seasonId=s.id"
       
        try:
            performanceResult = db.execute(performanceSelect)
            db.close()
        except:
            print performanceSelect + ' failed'
            db.close()
            return DB_ERROR
       
        if performanceResult.rowcount != 1:
            print performanceSelect
            print performanceResult.rowcount
            return DB_ERROR

        performance = performanceResult.first()
        
        performancePage = HTML_HEADER

        performancePage += '<h2>' + performance['name'] + '</h2>'
        performancePage += '<h3><a href="/team/' + str( performance['franchiseId'] ) + '">' +  performance['ownerName'] + '</a>'
        performancePage += ' -- Week ' + str( performance['weekNumber'] ) + ', ' + str( performance['year'] ) + '</h3>'
       
        statFields = positionPlayerStats
        if performance['position'] == 'K':
            statFields = kickerStats
        elif performance['position'] == 'D/ST':
            statFields = defenseStats

        performancePage += '<table class="table table-hover">'
        for stat in statFields:
            performancePage += '<tr><td>' + stat + '</td>'
            performancePage += '<td>' + str( performance[stat] ) + '</td></tr>'
        performancePage += '</table>'
        
        performancePage += HTML_FOOTER
        return performancePage

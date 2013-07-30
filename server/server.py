import web
from sqlalchemy import *
import sys
execfile('src/htmlSkeleton.py')
execfile('src/common.py')

urls = (
    '/', 'standings',
    '/team/([1-9][0-9]?)', 'team',
    '/game/([1-9][0-9]*)', 'game',
    '/performance/([1-9][0-9]*)', 'performance',
    '/backseat/([1-9][0-9]*)/([1-9][0-9]*)', 'backseatCoach'
)

app = web.application( urls, globals() )

execfile('src/standings.py')
execfile('src/team.py')
execfile('src/game.py')
execfile('src/performance.py')
execfile('src/backseatCoach.py')

if __name__ == "__main__":
    app.run()

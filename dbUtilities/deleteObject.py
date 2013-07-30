from optparse import OptionParser
import requests 
from sqlalchemy import *

parser = OptionParser()
parser.add_option('-i', '--id', dest='id',
        help='enter id of object you would like to delete')
parser.add_option('-t', '--type', dest='type',
        help='enter type of object you would like to delete')
(options, args) = parser.parse_args()

db = create_engine("mysql://javi:cs3200@localhost/copy").connect()

delete = 'DELETE FROM ' + options.type + ' WHERE id=' + options.id
print delete

try:
    db.execute(delete)
except:
    print 'an error occurred'


import json

with open("rating_database.json", "r") as f:
    db = json.loads( ''.join( f.readlines() ) )

for k,v in db['ign']['ratings'].items():
    print(k+" : "+str(v))

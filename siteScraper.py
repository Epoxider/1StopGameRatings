import bs4 as bs
from lxml import etree
import urllib.request
import time
import re
import json
import sys

# 
#   386070,
#   Planetary Annihilation: TITANS,
#   Action/Strategy,
#   $39.99,
#   https://steamcdn-a.akamaihd.net/steam/apps/386070/header.jpg?t=1564246041,
#   https://store.steampowered.com/app/386070,
#   Planetary Annihilation Inc,
#   Planetary Annihilation Inc,"Aug 18, 2015"


def addRating(game, rating):
    db[game] = rating


def get_IGN_Review(game):
    try:
        ignSauce  = urllib.request.urlopen('https://www.ign.com/games/'+game).read()
        ignSoup = bs.BeautifulSoup(ignSauce, 'lxml')
        rating = ignSoup.find("span", {"class": "hexagon-content"})

        try:
            rating = float(rating.text)
            rating
        except Exception as e:
            rating = rating.text

        return rating

    except Exception as e:
        return -1.0


def print_IGN_Review(game):
    gameRating = get_IGN_Review(game)
    print(gameRating)
"""
print_IGN_Review('overwatch')
print_IGN_Review('the-last-of-us')
print_IGN_Review('world-of-warcraft')
"""


def get_PCGamer_Review(game):
    try:
        pcSauce  = urllib.request.urlopen('https://www.pcgamer.com/'+game+'-review/').read()
        pcSoup = bs.BeautifulSoup(pcSauce, 'lxml')

        rating = pcSoup.find("span", {"class": "score score-long"})

        try:
            rating = float(rating.text)
            rating /= 10.0
        except Exception as e:
            rating = rating.text

        return rating

    except Exception as e:
        return -1.0


def print_PC_Review(game):
    gameRating = get_PCGamer_Review(game)
    print(gameRating)

"""
print_PC_Review('overwatch')
print_PC_Review('battlefield-5')
print_PC_Review('the-last-of-us')
"""

db = {
         'ign' : {
             'ratings' : {},
             'not_found' : {},
             'no_rating' : {},
         },
         'pc_gamer' : {
             'ratings' : {},
             'not_found' : {},
             'no_rating' : {},
         },
         'meta_critic' : {
             'ratings' : {},
             'not_found' : {},
             'no_rating' : {}
         },
}

def putRating( ratingSite, gameRating, gameName, fullName ):
    if not isinstance(gameRating, float):
        # print( "\tNO RATING FOUND at "+ratingSite+" : "+str(gameRating)+" for "+fullName)
        db[ratingSite]['no_rating'][fullName] = {'rating' : gameRating, 'search_name' : gameName}
    else:
        if gameRating < 0:
            db[ratingSite]['not_found'][fullName] = {'search_name' : gameName}
        else:
            print("\nFOUND at "+ratingSite+" : "+ gameName+" : "+str(gameRating))
            db[ratingSite]['ratings'][fullName] = {'rating' : gameRating, 'search_name' : gameName}

            # Save after every rating found... in case program crashes
            with open("rating_database.json", "w") as f:
                f.write( json.dumps(db) )

def processGameList(db):

    with open("games.csv", "r") as f:
        line = f.readline()
        i = 0
        while line:
            sys.stdout.write(".")
            sys.stdout.flush()
            i += 1
            parts = line.split(',')
            fullName = parts[1]
            noSymbolsLine = re.sub('[^A-Za-z0-9 ]+', '', fullName).lower()
            gameName = re.sub(" ","-",noSymbolsLine)

            ignRating = get_IGN_Review(gameName)
            putRating('ign', ignRating, gameName, fullName)

            pcGamerRating = get_PCGamer_Review(gameName)
            putRating('pc_gamer', pcGamerRating, gameName, fullName)

            line = f.readline()



processGameList(db)

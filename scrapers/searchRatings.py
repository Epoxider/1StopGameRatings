import json
import sys


def searchForGames(minRating):

    with open("rating_database.json", "r") as f:
        ratingsDict = json.loads(''.join( f.readlines() ))

    for gameSite, siteDict in ratingsDict.items():
        print( "Site: "+gameSite)
        for game, ratingAndSearchNameDict in siteDict['ratings'].items():
            rating = ratingAndSearchNameDict['rating']
            if rating >= minRating:
                print("\tGame: "+game+", rating: "+str(rating))



searchForGames(9.5)

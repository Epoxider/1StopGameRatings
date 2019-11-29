import bs4 as bs
from lxml import etree
import urllib.request
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


def getIGNReview(game):
    try:
        ignURL = 'https://www.ign.com/games/'+game
        ignSauce  = urllib.request.urlopen(ignURL).read()
        ignSoup = bs.BeautifulSoup(ignSauce, 'lxml')
        rating = ignSoup.find("span", {"class": "hexagon-content"})

        try:
            rating = float(rating.text)
        except Exception:
            rating = rating.text
        if rating == 'nr' or rating == 'NR':
            return -1.0, ''
        return rating, ignURL

    except Exception:
        return -1.0, ''


def printIGNReview(game):
    gameRating = getIGNReview(game)
    print(gameRating)
"""
print_IGN_Review('overwatch')
print_IGN_Review('the-last-of-us')
print_IGN_Review('world-of-warcraft')
"""


def getPCGamerReview(game):
    try:
        pcURL = 'https://www.pcgamer.com/'+game+'-review/'
        pcSauce  = urllib.request.urlopen(pcURL).read()
        pcSoup = bs.BeautifulSoup(pcSauce, 'lxml')

        rating = pcSoup.find("span", {"class": "score score-long"})

        try:
            rating = float(rating.text)
            rating /= 10.0
        except Exception:
            rating = rating.text
        return rating, pcURL

    except Exception:
        return -1.0, ''


def printPCReview(game):
    gameRating = getPCGamerReview(game)
    print(gameRating)

"""
print_PC_Review('overwatch')
print_PC_Review('battlefield-5')
print_PC_Review('the-last-of-us')
"""


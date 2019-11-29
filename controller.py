from flask import Flask, render_template, url_for, request
from flask_paginate import Pagination, get_page_args
import whoosh
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from whoosh import qparser
# from whoosh_search.py import whooshSearcher
from custom_search import customSearcher
import csv

app = Flask(__name__)
app.template_folder = 'templates'


@app.route('/', methods=['GET', 'POST'])
@app.route('/home/', methods=['GET', 'POST'])
def home():
	return render_template('home.html')

@app.route('/aboutus/')
def aboutus():
	return render_template('aboutus.html')

@app.route('/results/', methods=['GET', 'POST'])
def results():
	# global MyWhooshSearcher
	global MyCustomSearcher
	if request.method == 'POST':
		data = request.form
	else:
		data = request.args

	query = data.get('searchterm')

	# TODO: Search
	customRank = data.get('searchtype')
	if customRank:
		ids, names, ratings = MyCustomSearcher.search(query)
	# else:
	# 	results = MyWhooshSearcher.search(query)

	page, per_page, offset = get_page_args(page_parameter='page',per_page_parameter='per_page')

	results = [ids, names, ratings]

	total = len(results[0])

	pagination_results = zip(results[0][offset: offset + per_page], results[1][offset: offset + per_page], results[2][offset: offset + per_page]) 

	pagination = Pagination(page=page, per_page=per_page, total=total, css_framework="bootstrap4")
 
	return render_template('home.html', query=query, results=pagination_results, per_page=per_page, pagination=pagination)

@app.route('/game/', methods=['GET', 'POST'])
def game():
	print(request.args)
	data = request.args
	gameid = data.get('game')
	
	# TODO: Use gameID to get game data
	# gameInfo = getGameInfo(gameid)

	# TODO: Use game data to get top 3 related games
	# related_games = MyWhooshSearcher.getRelatedGames(gameInfo["genres"], gameInfo["price"], gameInfo["developer"], gameInfo["release_date"])

	# TODO: Pass all game data to the game page
	# return render_template('gamepage.html', title=gameInfo["title"], description=gameInfo["description"], genres=gameInfo["genres"], price=gameInfo["price"], image=gameInfo["image"], steam_url=gameInfo["steam_url"], developer=gameInfo["developer"], publisher=gameInfo["publisher"], release_date=gameInfo["release_date"], metacritic_score=gameInfo["metacritic_score"], metacritic_url=gameInfo["metacritic_url"], ign_score=gameInfo["ign_score"], ign_url=gameInfo["ign_url"], pcgamer_score=gameInfo["pcgamer_score"], pcgamer_url=gameInfo["pcgamer_url"], average=gameInfo["average"] )
	return render_template('gamepage.html', gameid=gameid)

def getGameInfo(gameID):
	with open('db/games.csv', 'r') as f:
		gameReader = csv.reader(f)
		for row in gameReader:
			if row[0] == str(gameID):
				f.close()
				return row
	f.close()
	return None

def getScoreInfo(gameID):
	with open('db/scores.csv', 'r') as f:
		gameReader = csv.reader(f)
		for row in gameReader:
			if row[0] == str(gameID):
				f.close()
				return row
	f.close()
	return None

if __name__ == '__main__':
	# TODO: Initialize two search classes and create indices for both
	# global MyWhooshSearcher
	global MyCustomSearcher

	# MyWhooshSearcher = whooshSearcher()
	# MyWhooshSearcher.index()

	MyCustomSearcher = customSearcher()
	MyCustomSearcher.index()
	app.run(debug=True)

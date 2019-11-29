from flask import Flask, render_template, url_for, request
from flask_paginate import Pagination, get_page_args
from custom.custom_search import customSearcher
from searcher_whoosh.whoosh_search import WhooshSearch
import csv

print("Building Whoosh index.... takes a while")
totalResults = 50
global_whoosh = WhooshSearch(totalResults)
print("Done building Whoosh index")

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
	global MyCustomSearcher
	global global_whoosh
	if request.method == 'POST':
		data = request.form
	else:
		data = request.args

	query = data.get('searchterm')

	if data.get('searchtype') == '0':
	    results = global_whoosh.run_search(query)
	else:
	    results = MyCustomSearcher.search(query)

	page, per_page, offset = get_page_args(page_parameter='page',per_page_parameter='per_page')

	total = len(results[0])

	pagination_results = zip(results[0][offset: offset + per_page], results[1][offset: offset + per_page], results[2][offset: offset + per_page]) 

	pagination = Pagination(page=page, per_page=per_page, total=total, css_framework="bootstrap4")
 
	return render_template('home.html', query=query, results=pagination_results, per_page=per_page, pagination=pagination)

@app.route('/game/', methods=['GET', 'POST'])
def game():
	print(request.args)
	data = request.args
	gameid = data.get('game')
	
	gameInfo = MyCustomSearcher.getDocInfo(gameid)
	metacriticScore = gameInfo[10]
	if float(metacriticScore) == -1:
		metacriticScore = 'N/A'
	ignScore = gameInfo[12]
	if float(ignScore) == -1:
		ignScore = 'N/A'
	pcgamerScore = gameInfo[14]
	if float(pcgamerScore) == -1:
		pcgamerScore = 'N/A'
	averageScore = gameInfo[16]
	if float(averageScore) == -1:
		averageScore = 'N/A'


	relatedGameIDS = global_whoosh.getRelatedGames(gameid, gameInfo[3], gameInfo[4], gameInfo[7], gameInfo[9])
	relatedGames = []
	for relatedGameID in relatedGameIDS:
		relatedGameTitle = MyCustomSearcher.getDocInfo(relatedGameID)[1]
		relatedGames.append((relatedGameID, relatedGameTitle))

	return render_template('gamepage.html', title=gameInfo[1], description=gameInfo[2], genres=gameInfo[3], price=gameInfo[4], image=gameInfo[5], steam_url=gameInfo[6], developer=gameInfo[7], publisher=gameInfo[8], release_date=gameInfo[9], metacritic_score=metacriticScore, metacritic_url=gameInfo[11], ign_score=ignScore, ign_url=gameInfo[13], pcgamer_score=pcgamerScore, pcgamer_url=gameInfo[15], average=averageScore, related_games=relatedGames )

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

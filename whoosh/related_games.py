import csv
import whoosh
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from whoosh import qparser

class whooshSearcher(object):

	def __init__(self):
		super(whooshSearcher, self).__init__()
		
	def getRelatedGames(self, gameID, genres, price, developer, date):
		titles = list()
		urls = list()

		with self.indexer.searcher() as search:
			query = "price:(" + price +") OR genres:(" + genres +") OR developer:(" + developer + ") OR date:(" + date + ") NOT id:" + str(gameID)
			parser = MultifieldParser(['genres', 'price', 'developer', 'date'], schema=self.indexer.schema) 
			query = parser.parse(query)
			results = search.search(query, limit=3)
			
			for x in results:
				titles.append(x['title'])
				urls.append(x['url'])
				
		return titles, urls

	def index(self):
		schema = Schema(id=ID(stored=True), title=TEXT(stored=True), genres=TEXT(stored=True), price=TEXT(stored=True), url=TEXT(stored=True), developer=TEXT(stored=True), date=TEXT(stored=True))
		indexer = create_in('indexdir', schema)
		writer = indexer.writer()
		# Change file path
		f = open('db/games.csv', 'r')
		with f:
			reader = csv.reader(f)
			# Read each row and add specific columns to the index
			for row in reader:
				if len(row) is 10 and row[0] is not 'Id':
					writer.add_document(id=row[0], title=row[1], genres=row[3], price=row[4], url=row[6], developer=row[7], date=row[9])
		f.close()
		writer.commit()

		self.indexer = indexer

def related_results(gameID, genres, price, developer, release_date):
	global searcher

	titles, urls = searcher.getRelatedGames(gameID, genres, price, developer, release_date)
	return titles, urls

def findGame(gameID):
	f = open('db/games.csv', 'r')
	with f:
		reader = csv.reader(f)
		for row in reader:
			if row[0] == str(gameID):
				f.close()
				return row
	f.close()
	return None
		

if __name__ == '__main__':
	global searcher
	
	searcher = whooshSearcher()
	searcher.index()

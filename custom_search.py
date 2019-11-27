import csv
import json

class customSearcher(object):
	"""docstring for customSearcher"""
	def __init__(self):
		super(customSearcher, self).__init__()
		
	def search(self, query):
		# Searches the database using the user's input
		# Returns the results as 3 lists: titles, ratings, and 
		ids = list()
		titles = list()
		ratings = list()

		# Parse the query and search
		# with self.indexer.searcher(weighting=scoring.BM25F()) as search:
		# 	query = MultifieldParser(['title', 'rating', 'gameid'], schema=self.indexer.schema)
		# 	query = query.parse(query)
		# 	results = search.search(query, limit=nResults)
		# 	for x in results:
		# 		titles.append(x['title'])
		# 		ratings.append(x['rating'])
		# 		ids.append(x['url'])
			
		return ids, titles, ratings

	def processDoc(self, docID, title, desc):
		# For each document in games.csv:
		#	title = document[1]
		#	description = document[2]
		#	terms = title + " " + description
		#	terms.split(" ")
		#	For each term in document:
		#		if term in invertedIndex
		#			if docID in invertedIndex["term"]:
		#				continue
		#			newEntry = {
		# 				title: title.count(term),
		#				desc: description
		# 			}
		#			invertedIndex["term"].update(
		# 									{docID : newEntry})
		#			else:
		#				newEntry = {
		#	 				title: title.count(term),
		#					desc: description
		# 				}
		#				invertedIndex.update(
		# 							{term: {docID : newEntry}})
		#
		title = title.lower()
		desc = desc.lower()
		terms = title + " " + desc
		terms.split(" ")
		for term in terms:
			if term in self.invertedIndex:
				if docID in self.invertedIndex["term"]:
					continue
				newEntry = {
					"title": title.count(term),
					"desc": desc.count(term)
				}
				self.invertedIndex["term"].update({docID : newEntry})
			else:
				newEntry = {
					"title": title.count(term),
					"desc": desc.count(term)
				}
				self.invertedIndex.update(
							{term: {docID : newEntry}})


	def index(self):
		# Creates an index for the dataset		

		self.invertedIndex = {}

		# Write to the index from data.csv
		f = open('db/games.csv', 'r')
		with f:
			reader = csv.reader(f)
			# Read each row and add specific columns to the index
			for row in reader:
				if len(row) is 10 and row[0] is not 'Id':
					self.processDoc(row[0], row[1], row[2])
		print(self.invertedIndex)
		# self.indexer = indexer
		return

if __name__ == '__main__':
	global myCustomSearcher
	myCustomSearcher = customSearcher()
	myCustomSearcher.index()
	results = myCustomSearcher.search("Simulator")
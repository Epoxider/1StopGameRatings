import csv
import re
import math

class customSearcher(object):
	"""docstring for customSearcher"""
	def __init__(self):
		super(customSearcher, self).__init__()
		
	def search(self, query):
		# Searches the database using the user's input
		# Returns the results as 3 lists: ids, titles, and ratings

		query = self.processTerms(query)

		results = self.bm25(query)

		ids = []
		names = []
		ratings = []
		for docID in results:
			docInfo = self.getDocInfo(docID)
			ids.append(docInfo[0])
			names.append(docInfo[1])
			rating = docInfo[16]
			rating = float(rating)
			if rating == -1:
				ratings.append('Not Rated')
			else: 
				ratings.append(round(rating, 1))

		return ids, names, ratings

	def bm25(self, query):
		# Returns a sorted list of results for the given query
		# Ranks documents using a modified BM25 algorithm
		rankedDocs = {}

		# Following values are used in ranking later on
		N = self.docCount
		k_1 = 1.2            
		k_2 = 500				
		b = 0.75  
		titleWeight = 0.75
		descWeight = 0.25

		for term in query:
			if term not in self.invertedIndex:
				continue
			termIndex = self.invertedIndex[term]
			df_t = len(termIndex)
			qf_t = query.count(term)

			for doc in termIndex:
				titleRank = 0
				descRank = 0
				titleFreq = termIndex[doc]["title"]
				descFreq = termIndex[doc]["desc"]
				titleCount = self.docInfo[doc]["titleCount"]
				descCount = self.docInfo[doc]["descCount"]
				averageTitleCount = self.docInfo["averageTitleCount"]
				averageDescCount = self.docInfo["averageDescCount"]

				if titleFreq:
					df_t = len(termIndex)
					qf_t = query.count(term)
					invertedDocFreq = math.log((N - df_t + 0.5)/(df_t + 0.5))
					termFreq = ((k_1+1)*titleFreq)/((k_1*(1-b)+b*titleCount/averageTitleCount)+titleFreq)
					queryTermFreq = (k_2+1)*qf_t/(k_2+qf_t)
					titleRank += invertedDocFreq * termFreq * queryTermFreq

				if descFreq:
					df_t = len(termIndex)
					qf_t = query.count(term)
					invertedDocFreq = math.log((N - df_t + 0.5)/(df_t + 0.5))
					termFreq = ((k_1+1)*descFreq)/((k_1*(1-b)+b*descCount/averageDescCount)+descFreq)
					queryTermFreq = (k_2+1)*qf_t/(k_2+qf_t)
					descRank += invertedDocFreq * termFreq * queryTermFreq

				rank = titleWeight * titleRank + descWeight * descRank
				if doc in rankedDocs:
					rankedDocs[doc] += rank
				else:
					rankedDocs.update({ doc : rank })

		# Sort results to from highest rank to lowest rank
		orderedDocs = sorted(rankedDocs, key=rankedDocs.get, reverse=True)
		return orderedDocs

	def getDocInfo(self, docID):
		return self.docInfo[docID]["data"]

	def processDoc(self, doc):
		# Add the document information to docInfo and add terms/frequencies to the invertedIndex
		docID = doc[0]
		title = self.processTerms(doc[1])
		desc = self.processTerms(doc[2])

		# Add information to docInfo
		self.titleCount += len(title)
		self.descCount += len(desc)
		self.docInfo.update(
			{ docID : 
				{ 
					"titleCount" : len(title),
					"descCount" : len(desc),
					"data" : doc
				}
			}
		)

		# Add terms to invertedIndex
		terms = title + desc
		for term in terms:
			if term in self.invertedIndex:
				if docID in self.invertedIndex[term]:
					continue
				newEntry = {
					"title": title.count(term),
					"desc": desc.count(term)
				}
				self.invertedIndex[term].update({docID : newEntry})
			else:
				newEntry = {
					"title": title.count(term),
					"desc": desc.count(term)
				}
				self.invertedIndex.update(
							{term: {docID : newEntry}})
		return

	def index(self):
		# Creates an index for the dataset
		# Creates a dictionary of document info
		self.invertedIndex = {}
		self.docInfo = {
			"averageTitleCount" : 0,
			"averageDescCount" : 0
		}

		# Write to the index from games.csv
		self.addDocuments()

		# Write scores to each doc in docInfo
		self.addScores()

		return

	def addDocuments(self):
		# Read documents, add terms to invertedIndex, populate docInfo
		self.titleCount = 0
		self.descCount = 0
		self.docCount = 0

		with open('db/games.csv', 'r') as f:
			reader = csv.reader(f)
			for row in reader:
				if len(row) is 10 and row[0] is not 'Id':
					self.processDoc(row)
					self.docCount += 1
		f.close()

		# Add average lengths for use 
		self.docInfo["averageTitleCount"] = self.titleCount / self.docCount
		self.docInfo["averageDescCount"] = self.descCount / self.docCount


	def addScores(self):
		with open('db/scores.csv', 'r') as f:
			reader = csv.reader(f)
			for row in reader:
				if len(row) is 8 and row[0] is not 'Id':
					self.docInfo[row[0]]["data"] += row[1:]
		f.close()

	def processTerms(self, terms):
		# Convert terms to lowercase, remove all non-alphanumerical characters, and split into an array
		terms = terms.lower()
		terms = re.sub('[^a-z0-9 ]+', '', terms)
		terms = terms.split()
		newTerms = terms.copy()
		prevTerm = None

		# N-Grams: compute N-grams and add the list of terms
		for term in terms:
			if not prevTerm:
				prevTerm = term
			else:
				newTerms.append(prevTerm + " " + term)
				prevTerm = term
		return newTerms


if __name__ == '__main__':
	global myCustomSearcher
	myCustomSearcher = customSearcher()
	myCustomSearcher.index()

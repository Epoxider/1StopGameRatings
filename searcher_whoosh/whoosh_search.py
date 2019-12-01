from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh.index import create_in
from whoosh.analysis import StemmingAnalyzer
from whoosh.qparser import MultifieldParser
from whoosh.analysis import NgramWordAnalyzer
import os

import json
#import csv exmple in releated games.
#make whoosh into a class to make it easier to pass into controller.py

class WhooshSearch(object):

    def __init__(self, max_results=50):
        self.max_results = max_results
        print("\nBuilding schema... have patience")
        self.indexer = self.buildSchema()
        print("\nFinished building schema")

    def buildSchema(self):
        ngram_analyzer = False

        if ngram_analyzer:
            analyzer = NgramWordAnalyzer(minsize = 3)
            schema = Schema( id=ID(stored=True),
                     title=TEXT(analyzer = analyzer,stored=True),
                     description=TEXT(analyzer = analyzer,stored=True),
                     IGN_rating=TEXT(stored=True),
                     PCGamer_rating=TEXT(stored=True),
                     MetaCritic_rating=TEXT(stored=True),
                     average_rating=TEXT(stored=True),
                     )
        else:
            schema = Schema( id=ID(stored=True),
                     title=TEXT(stored=True),
                     description=TEXT(stored=True),
                     IGN_rating=TEXT(stored=True),
                     PCGamer_rating=TEXT(stored=True),
                     MetaCritic_rating=TEXT(stored=True),
                     average_rating=TEXT(stored=True),
                     )
    
        if os.sep in __file__:
            path_parts = __file__.split(os.sep)[:-1]
            base_path = os.sep.join(path_parts)
        else:
            base_path = "."

        index_path = base_path + os.sep + "indexdir"

        indexer = create_in(index_path, schema)
        writer = indexer.writer()
    
        ratings_db = {}
        with open(base_path+os.sep+"../db/scores.csv", "r") as f:
            ratings_titles = f.readline()

            for line in f:
                parts = line.strip().split(",")

                appID = parts[0]
                meta_rating = parts[1]
                if float(meta_rating) < 0.0:
                    meta_rating = "No Rating"
                meta_url = parts[2]
                ign_rating = parts[3]
                if float(ign_rating) < 0.0:
                    ign_rating = "No Rating"
                ign_url = parts[4]
                pcgamer_rating = parts[5]
                if float(pcgamer_rating) < 0.0:
                    pcgamer_rating = "No Rating"
                pcgamer_url = parts[6]
                average_score = parts[7]
                if float(average_score) < 0.0:
                    average_score = "No Rating"

                ratings_db[appID] = {
                        'meta' : meta_rating,
                        'meta-url' : meta_url,
                        'ign' : ign_rating,
                        'ign-url' : ign_url,
                        'pcgamer' : pcgamer_rating,
                        'pcgamer-url' : pcgamer_url,
                        'avg-score' : average_score
                }

        with open(base_path+os.sep+"../db/games.csv", "r") as f:
            # Consume the title line
            titles = f.readline()
    
            for line in f:
                parts = line.strip().split(',')

                appID = parts[0]
                gameName = parts[1]
                description = parts[2]

                gameName = gameName.replace("&#44;", ",") 
                description = description.replace("&#44;", ",") 
                if appID in ratings_db:
                    writer.add_document(id=appID,
                                title=gameName, 
                                description=description,
                                IGN_rating=ratings_db[appID]['ign'],
                                PCGamer_rating=ratings_db[appID]['pcgamer'],
                                MetaCritic_rating=ratings_db[appID]['meta'],
                                average_rating=ratings_db[appID]['avg-score']
                           )
    
        writer.commit()
    
        return indexer
    
    def run_search(self, searchTerm):
    
        ids = []
        names = []
        ratings = []

        with self.indexer.searcher() as search:
            query = MultifieldParser(["title", "description"], schema=self.indexer.schema)
            query = query.parse(searchTerm)
    
            results = search.search(query, limit=self.max_results)

            for result in results:

                ign_rating = result['IGN_rating']
                pcgamer_rating = result['PCGamer_rating']
                metacritic_rating = result['MetaCritic_rating']

                ids.append( result['id'] )
                names.append( result['title'] )
                ratings.append( result['average_rating'] )

        return [ tuple(ids), tuple(names), tuple(ratings) ]
    
if __name__ == "__main__":
    whoosher = WhooshSearch(max_results=100)
    userPrompt = "\nEnter search query (<RETURN> to quit): "
    userInput = input(userPrompt)

    while userInput != "":
        results = whoosher.run_search(userInput)

        num = len(results[0])
        print("Results of looking for '"+userInput+"'")
        print("Total responses: "+str(num)+"\n"+"-"*60)
        for i in range(num):
            print( results[0][i] + " : " + results[2][i] + " : " + results[1][i] )

        userInput = input(userPrompt)


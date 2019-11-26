from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh.index import create_in
from whoosh.analysis import StemmingAnalyzer
from whoosh.qparser import MultifieldParser

import json

numQueries = 20

def buildSchema():

    print("Creating Schema")
    schema = Schema( id=ID(stored=True),
                 title=TEXT(stored=True),
                 description=TEXT(stored=True) )

    indexer = create_in("indexdir", schema)
    writer = indexer.writer()

    with open("../db/games.csv", "r") as f:
        # Consume the title line
        titles = f.readline()

        for line in f:
            parts = line.split(',')
            appID = parts[0]
            gameName = parts[1]
            description = parts[2]

            writer.add_document(id=appID,
                            title=gameName, 
                            description=description)

    writer.commit()

    return indexer

def doSearch(indexer, searchTerm):

    with indexer.searcher() as search:
        query = MultifieldParser(["title", "description"], schema=indexer.schema)
        query = query.parse(searchTerm)

        print("query is "+str(query))
        results = search.search(query, limit=numQueries)

        print("Results of looking for '"+searchTerm+"'")
        print("Total responses: "+str(len(results))+"\n"+"-"*60)
        for result in results:

            myTuple = ( result['id'], result['title'], "rank="+str(result.rank), result.get('description', ""))
            print(str(myTuple))
            print("\n")


if __name__ == "__main__":
    indexer = buildSchema()
    userPrompt = "\nEnter search query (<RETURN> to quit): "
    userInput = input(userPrompt)
    while userInput != "":
        doSearch(indexer, userInput)
        userInput = input(userPrompt)


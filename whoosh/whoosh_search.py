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

    COMMENT_FIELD = 2  # 0-based
    FIELDS_AFTER_COMMENT = 8

    with open("../db/games.csv", "r") as f:
        # Consume the title line
        titles = f.readline()

        for line in f:
            # There can be commends in the description (3rd field) and also comments
            # in the release date (last field).  Deal with this by just stripping
            # off the left 2 fields first (id, name), then strip from the right
            # side.  If the last field ends with '"', then there is an extra comma.
            leftparts = line.split(',',COMMENT_FIELD)
            rightparts = leftparts[2].rsplit(",",FIELDS_AFTER_COMMENT-1)

            # If the release date ends with '"', there is a comma in this field,
            # so we have an extra command to deal with e.g. extra field
            if rightparts[-1].strip().endswith('"'):
                rightparts = leftparts[2].rsplit(",",FIELDS_AFTER_COMMENT)

            appID = leftparts[0]
            gameName = leftparts[1]
            description = rightparts[0].strip('"')

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


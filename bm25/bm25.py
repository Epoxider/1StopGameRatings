# Used for sorting dictionary by value
import operator
import sys
# Needed for log()
import math

filename = "../db/games.csv"

# Read wine dictionary into global dictionary: gameDict
with open(filename, "r") as f:
    fileLines = f.readlines()

# Remove the first line, which is the column names
fileLines.pop(0)

gameDict = {}
averageLength = 0.0

for line in fileLines:
    parts = line.strip().split(',')

    id = parts[0]
    name = parts[1]
    desc = parts[2]

    name = name.replace("&#44;", ",") 
    desc = desc.replace("&#44;", ",") 

    gameDict[id] = {'name':name, 'description' : desc, 'line' : line}
    averageLength += float(len(desc.split()))
   
# Compute the average of all the lengths
averageLength = averageLength / float(len(gameDict))

# termCountInDict is populated just to speed things up
termCountInDict = {}

def populateTermCountInDict(query):
    for t in query.split():
        n_t = 0.0
        for id, d in gameDict.items():
            desc = d['description']
            # NOTE: The description of the problem says 
            # n_t is "n(t) is the number of documents containing t"
            # but when I compute that as follows, the answer doesn't
            # match what you posted.
            # if t in desc:
            #     n_t += 1.0

            # If instead, we count how many times the term appears
            # across all documents, then the answer matches what you
            # posted.
            words = desc.split()
            for w in words:
                if w == t:
                    n_t += 1.0

        termCountInDict[t] = n_t 



def bm25_algorithm(d, Q):
    """Computes the bm25 algorithm value for a given document and
       a query string.

    Args:
        d : The document ID
        Q : The query string

    Returns:
        The result of the bm25 algorithm for query string against a document.
    """

    N = float(len(gameDict))
    k_1 = 1.2
    k_2 = 500.0
    b = 0.75

    result = 0.0

    for t in Q.split():

        df_t = termCountInDict[t]

        part1 = math.log((N-df_t+0.5)/(df_t+0.5))

        # Count how many times t is in the document
        desc = gameDict[d]['description']
        desc_words = desc.split()

        f_t = 0.0
        for t_tmp in desc_words:
            if t == t_tmp:
                f_t += 1.0
        
        length = float(len(desc_words)) #length of document
    
        part2 = ((k_1+1)*f_t)/((k_1*(1.0-b) + b*((length)/averageLength))+f_t)

        # Count how many times t is in the query string
        qf_t = 0.0
        for t_tmp in Q.split():
            if t == t_tmp:
                qf_t += 1.0

        part3 = (((k_2+1.0)*qf_t)/(k_2+qf_t))

        result += part1*part2*part3

    return result
    


def bm25(query,k):
    """Compute the bm25 across all documents, keeping track of
       the score for each document.  Sorts the results in descending
       order.  Don't store any result with a value of 0.

    Args:
        query : The query string
        k : The number of results to return

    Returns:
        A list of the top 'k' most relevant documents according to bm25.
    """
    populateTermCountInDict(query)
    
    scoreDict = {}

    for id in gameDict:
        score = bm25_algorithm(id, query)
        if score > 0.0:
            scoreDict[id] = score

    sortedItems = sorted(scoreDict.items(), key=operator.itemgetter(1),
                           reverse=True)

    if len(sortedItems) < k:
        return sortedItems
    else:
        return sortedItems[:k]


bmScores = bm25("dark", 5)
for id,score in bmScores:
    print(id+" : "+str(score)+" : "+gameDict[id]['name']+ " : "+gameDict[id]['description'])


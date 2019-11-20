from steam_scraper import getSteamInfo
from siteScraper import get_PCGamer_Review, get_IGN_Review
import csv
import requests
from bs4 import BeautifulSoup
from lxml import etree

def getPage(url):
	page = requests.get(url)
	return page

def strip_ns(tree):
    for node in tree.iter():
        try:
            has_namespace = node.tag.startswith('{')
        except AttributeError:
            continue
        if has_namespace:
            node.tag = node.tag.split('}', 1)[1]

def getAppList():
    # Retrieves all steam appIDs

    appListURL = "http://api.steampowered.com/ISteamApps/GetAppList/v2/?key=STEAMKEY&format=xml"
    rawPageAppList = getPage(appListURL)

    root = etree.fromstring(rawPageAppList.content)
    strip_ns(root)
	
    appIDs = root.xpath('/applist/apps/app/appid/text()')
    appIDs.reverse()
    return appIDs

def convertTitleForReviewSites(title):
    # Returns a title that is formatted for use in the ratings scrapers

    reviewTitle = title.lower()
    reviewTitle = reviewTitle.replace(" ", "-")
    return reviewTitle


def main():
	# For each game: get steam data, ign ratings, and pc gamer ratings
	# Write this data to games.csv
	
    print("\nScraping for appIDs...")

    appIDs = getAppList()

    gamesFILE = open('../db/games.csv', 'w')
    scoresFILE = open('../db/scores.csv', 'w')

    with gamesFILE, scoresFILE:
        gameWriter = csv.writer(gamesFILE)
        scoreWriter = csv.writer(gamesFILE)

        # Write headers for the games.csv and scores.csv files
        gameWriter.writerow(["id","title","genres","price","image","steam_url","developer","publisher","release_date"])
        scoreWriter.writerow(["metacritic_score", "metacritic_url", "ign_score", "ign_url", "pcgamer_score", "pcgamer_url", "average"])

        for appID in appIDs:
            # Get Steam data
            result = getSteamInfo(appID)
            if not result:
                continue
            title, genres, price, img, url, dev, pub, date, meta_score, meta_url = result

            # Get Ratings and URLs
            reviewTitle = convertTitleForReviewSites(title)
            ign_score, ign_url = get_IGN_Review(reviewTitle)
            pcgamer_score, pcgamer_url = get_PCGamer_Review(reviewTitle)

            # Write to files
            gameWriter.writerow([appID, title, genres, price, img, url, dev, pub, date])
            scoreWriter.writerow([appID, meta_score, meta_url, ign_score, ign_url, pcgamer_score, pcgamer_url])

    gamesFILE.close()
    scoresFILE.close()
	
    return

if __name__ == '__main__':
	main()

from steam_scraper import getSteamInfo
from site_scraper import getPCGamerReview, getIGNReview
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
    reviewTitle = reviewTitle.replace(":", "")
    reviewTitle = reviewTitle.replace("- ", "")
    reviewTitle = reviewTitle.replace("\u00AE", "")
    reviewTitle = reviewTitle.replace("\u00A9", "")
    reviewTitle = reviewTitle.replace("\u2122", "")
    return reviewTitle

def calculateAverageRating(metacritic, ign, pcgamer):
    # Attempts to calculate a weighted average for ratings
    # If all are -1 (N/A), return -1
    if float(metacritic) < 0.0 and float(ign) < 0.0 and float(pcgamer) < 0.0:
        return -1.0
    metacritic_scale = 0.25*int(float(metacritic) >= 0.0)
    pcgamer_scale = 0.25*int(float(pcgamer) >= 0.0)
    ign_scale = 0.5*int(float(ign) >= 0.0)

    combined_scale = metacritic_scale + pcgamer_scale + ign_scale

    averageRating = metacritic_scale*metacritic + pcgamer_scale*pcgamer + ign_scale*ign
    averageRating /= combined_scale

    return averageRating

def main():
	# For each game: get steam data, ign ratings, and pc gamer ratings
	# Write this data to games.csv
	
    print("\nGetting appIDs...")

    appIDs = getAppList()

    gamesFILE = open('../db/games.csv', 'w')
    scoresFILE = open('../db/scores.csv', 'w')

    print("\nGetting game info...")

    with gamesFILE, scoresFILE:
        gameWriter = csv.writer(gamesFILE)
        scoreWriter = csv.writer(scoresFILE)

        # Write headers for the games.csv and scores.csv files
        gameWriter.writerow(["id","title","description","genres","price","image","steam_url","developer","publisher","release_date"])
        scoreWriter.writerow(["id", "metacritic_score", "metacritic_url", "ign_score", "ign_url", "pcgamer_score", "pcgamer_url", "average"])

        for appID in appIDs:
            # Get Steam data
            result = getSteamInfo(appID)
            if not result:
                continue
            title, description, genres, price, img, url, dev, pub, date, meta_score, meta_url = result
            title = title.replace(',', '&#44;').strip().strip('"')
            description = description.replace(',', '&#44;').strip().strip('"')
            genres = genres.replace(',', '&#44;').strip().strip('"')
            price = price.replace(',', '&#44;').strip().strip('"')
            img = img.replace(',', '&#44;').strip().strip('"')
            url = url.replace(',', '&#44;').strip().strip('"')
            dev = dev.replace(',', '&#44;').strip().strip('"')
            pub = pub.replace(',', '&#44;').strip().strip('"')
            date = date.replace(',', '&#44;').strip().strip('"')
            meta_url = meta_url.replace(',', '&#44;').strip().strip('"')

            meta_score = float(meta_score)
            if meta_score >= 0.0:
                meta_score /= 10.0

            # Get Ratings and URLs
            reviewTitle = convertTitleForReviewSites(title)
            ign_score, ign_url = getIGNReview(reviewTitle)
            pcgamer_score, pcgamer_url = getPCGamerReview(reviewTitle)
            average = calculateAverageRating(meta_score, ign_score, pcgamer_score)

            # Write to files
            gameWriter.writerow([appID, title, description, genres, price, img, url, dev, pub, date])
            scoreWriter.writerow([appID, meta_score, meta_url, ign_score, ign_url, pcgamer_score, pcgamer_url, average])

    gamesFILE.close()
    scoresFILE.close()
	
    return

if __name__ == '__main__':
	main()

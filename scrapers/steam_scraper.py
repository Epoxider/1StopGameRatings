import os
import sys
from bs4 import BeautifulSoup
from lxml import etree
import requests
import csv
import json
import time

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

def main():
    getAppListURL = "http://api.steampowered.com/ISteamApps/GetAppList/v2/?key=STEAMKEY&format=xml"
    steamURL = "https://store.steampowered.com/app/"
    appDataURL = "https://store.steampowered.com/api/appdetails?appids="
    ids = []
    names = []
    genres = []

	
    print("\nScraping for appIDs...")

    rawPageAppList = getPage(getAppListURL)

    root = etree.fromstring(rawPageAppList.content)
    strip_ns(root)
	
    appIDs = root.xpath('/applist/apps/app/appid/text()')
    appIDs.reverse()

    f = open('games.csv', 'w')

    with f:
        writer = csv.writer(f)

        # Write the headers for the csv file
        headers = ["id","title","genres","price","image","steam_page","developer","publisher","release_date"]
        writer.writerow(headers)

        for appID in appIDs:
            idStr = str(appID)
            row = [appID]
            dataPage = requests.get(appDataURL+idStr)
            print(dataPage.status_code)
            if dataPage.status_code == 429:
                time.sleep(200)
                dataPage = requests.get(appDataURL+idStr)
            if dataPage.status_code != 200:
                continue
            gameJSON = dataPage.json()
            if gameJSON[idStr]["success"] == True and gameJSON[idStr]["data"]["type"] == "game":
                row.append(gameJSON[idStr]["data"]["name"])
                if "genres" in gameJSON[idStr]["data"]:
                    genres = gameJSON[idStr]["data"]["genres"]
                    if len(genres) != 0:
                        isFirst = True
                        genreStr = genres[0]["description"]
                        for genre in genres:
                            if not isFirst:
                                genreStr = genreStr + "/" + genre["description"]
                            else:
                                isFirst = False    
                        row.append(genreStr)
                else:
                    row.append("")  
                if "price_overview" in gameJSON[idStr]["data"] and "final_formatted" in gameJSON[idStr]["data"]["price_overview"]:
                    row.append(gameJSON[idStr]["data"]["price_overview"]["final_formatted"])
                else: 
                    row.append("")

                row.append(gameJSON[idStr]["data"]["header_image"])
                row.append(steamURL+idStr)

                if "developers" in gameJSON[idStr]["data"] and len(gameJSON[idStr]["data"]["developers"]) != 0:
                    row.append(gameJSON[idStr]["data"]["developers"][0])
                
                if "publishers" in gameJSON[idStr]["data"] and len(gameJSON[idStr]["data"]["publishers"]) != 0:
                    row.append(gameJSON[idStr]["data"]["publishers"][0])

                if gameJSON[idStr]["data"]["release_date"]["coming_soon"]:
                    row.append("Unrealeased")
                else:
                    row.append(gameJSON[idStr]["data"]["release_date"]["date"])
                
                writer.writerow(row)

    f.close()
    print("Done!") 

if __name__ == '__main__':
	main()
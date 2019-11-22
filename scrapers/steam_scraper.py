import os
import sys
import requests
import json
import time

def getSteamInfo(appID):
    appDataURL = "https://store.steampowered.com/api/appdetails?appids="
    appID = str(appID)
    dataPage = requests.get(appDataURL+appID)

    # Check if there have been too many requests
    if dataPage.status_code != 200:
        # Try again after 200 seconds
        print("Error Code: " + str(dataPage.status_code) + " - Trying again...")
        time.sleep(200)
        dataPage = requests.get(appDataURL+appID)
        # If response is still bad, skip the game
        if dataPage.status_code != 200:
            print("Skipping game with appID #" + appID)
            return None
    
    gameJSON = dataPage.json()

    # Check API response
    if gameJSON[appID]["success"] == False or gameJSON[appID]["data"]["type"] != "game":
        return None

    # Title
    title = gameJSON[appID]["data"]["name"]

    # Description
    description = gameJSON[appID]["data"]["short_description"]

    # Genres (optional)
    if "genres" in gameJSON[appID]["data"]:
        genres = gameJSON[appID]["data"]["genres"]
        if len(genres) != 0:
            genreStr = genres[0]["description"]
            for i in range(1, len(genres)):
                genreStr = genreStr + "/" + genres[i]["description"]  
            genres = genreStr
    else:
        genres = ""

    # Price (optional)
    if "price_overview" in gameJSON[appID]["data"] and "final_formatted" in gameJSON[appID]["data"]["price_overview"]:
        price = gameJSON[appID]["data"]["price_overview"]["final_formatted"]
    else: 
        price = ""

    # Main image
    image = gameJSON[appID]["data"]["header_image"]
    
    # Steam URL
    url = "https://store.steampowered.com/app/"+appID

    # Developer (optional)
    if "developers" in gameJSON[appID]["data"] and len(gameJSON[appID]["data"]["developers"]) != 0:
        developers = gameJSON[appID]["data"]["developers"][0]
    else: 
        developers = ""
    
    # Publisher (optional)
    if "publishers" in gameJSON[appID]["data"] and len(gameJSON[appID]["data"]["publishers"]) != 0:
        publishers = gameJSON[appID]["data"]["publishers"][0]
    else:
        publishers = ""

    # Release Date
    if gameJSON[appID]["data"]["release_date"]["coming_soon"]:
        release_date = "Unrealeased"
    else:
        release_date = gameJSON[appID]["data"]["release_date"]["date"]

    # Metacritic Score and URL
    if "metacritic" in gameJSON[appID]["data"]:
        metacritic_score = float(gameJSON[appID]["data"]["metacritic"]["score"])
        metacritic_url = gameJSON[appID]["data"]["metacritic"]["url"]
    else: 
        metacritic_score = -1
        metacritic_url = ""
    
    return title, description, genres, price, image, url, developers, publishers, release_date, metacritic_score, metacritic_url
        
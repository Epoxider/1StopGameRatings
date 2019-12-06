# 1StopGameRatings (Final Project for CS 483)
### Created By: Rebekah Rolfe, Matthew Fritz, and Jacob van Tol

## Description
1StopGameRatings is a local web application that provides easy access to important game information. The popular search engine, Whoosh!, is integrated to return games efficiently and accurately. The site includes an average rating system based on three popular rating sites: IGN, PC Gamer, and Metacritic. 

## How to run
### Creating the database
1. In terminal, navigate to the project's 'scrapers' directory
2. Run the following command: python3 initialize_db.py
3. Wait...
4. Wait some more... (it takes about 8-10 hours to retrieve 10,000 games/ratings, depending on hardware and internet connection)
5. When you are tired of waiting, use Ctrl+C to exit the program
6. View results in the 'db' directory (game information is stored in games.csv, scores in scores.csv)

### Running the website
1. In terminal, navigate to the project
2. Run the following command: python3 controller.py
3. Wait for the indices to be created
4. Use the link that is outputted in the terminal to view the website

## Libraries and References
* Flask
* Whoosh!
* BeautifulSoup

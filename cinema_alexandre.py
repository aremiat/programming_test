"""
The page shown at the link below contains movies with some metadata of interest to our friend Quentin, a budding movie director.

https://www.listchallenges.com/100-must-see-movies-for-more-advanced-cinephiles

title
year
ranking
no_of_votes


Task
Using your preferred language and/or tools - write a program that parses this page and extracts the following data into two possible file formats

1 - A CSV file
2 - A HTML file with some style formatting applied - You can use a CSS framework like https://tailwindcss.com/docs to complete this task.


Include instructions on how to run your program including installing any dependencies.

Usage:

python cinema.py --format [ CSV | HTML ]

"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


url = 'https://www.listchallenges.com/100-must-see-movies-for-more-advanced-cinephiles'

# webscrapping technique, récup du title, year and ranking mais j'ai pas réussi le nombre de vote
def transform(url):
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    movies = soup.find_all('div', class_='item-name')
    rt_scores = soup.find_all('div', class_='item-rank')
    
    movie_data = []
    
    for movie in movies:  # itération pour recup titre et année
        movie_text = movie.get_text().strip()  # clean de la data remove les espaces blancs
        match = re.match(r'(.*?)\s*\((\d{4})\)', movie_text)
        if match:
            title, year = match.groups()
            movie_data.append((title.strip(), year))  # ajouter titre et année 
            
    scores = [score.get_text(strip=True) for score in rt_scores]
    
    combined_data = list(zip(movie_data, scores))
    df = pd.DataFrame([(*movie, score) for movie, score in combined_data], columns=['Title', 'Year', 'Ranking'])

    return df
    
pass

df = transform(url)

# Function to save data into CSV format
def save_as_csv(dataframe):
    dataframe.to_csv('movies.csv', index=False)
    
save_as_csv(df)

# Function to save data into HTML format
def save_as_html(dataframe):
    dataframe.to_html('movies.html', index=False, classes=['table', 'table-striped'])
    
save_as_html(df)
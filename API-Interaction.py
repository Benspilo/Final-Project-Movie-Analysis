import sqlite3
import json
import os
import requests
import bs4
import re


#IMDB API key: k_2rg9hfrx

use_key = "k_qmvwis56"

#https://imdb-api.com/API/Top250Movies/k_2rg9hfrx

'''
def get_movie_data(title):
    endpoint='https://www.omdbapi.com/'
    param = {}
    param['t'] = title
    param['r'] = 'json'
    this_page_cache = requests_with_caching.get(endpoint, params=param)
    return json.loads(this_page_cache.text)

    *
    No Api key was needed for this but for imbd we use 
    param[documentation for api key] = our api key
    then we can do requests or requests with caching (makes no difference here)
    and add params as shown above. 
'''
def setup_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def setup_IMDB_table(cur, conn):
    #CHANGE TO IF NOT EXISTS
    cur.execute("CREATE TABLE IF NOT EXISTS IMDB_data (Name TEXT PRIMARY KEY, id TEXT, Rank INTEGER , Year INTEGER, Rating NUMERIC)")
    conn.commit()

def setup_wiki_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Wiki_data (Name TEXT PRIMARY KEY, date TEXT, Budget TEXT, Box_office TEXT, Length TEXT)")

def get_wiki(wiki_html):
    url = wiki_html
    resp = requests.get(url)
    soup = bs4.BeautifulSoup(resp.content, "html.parser")
    table = soup.find('table', class_ = "infobox vevent")
    
    info = {}

    tag = table.find(text=re.compile(r'Budget'))
    budget = tag.parent.parent
    
    tag = table.find(text=re.compile(r'Box office'))
    box = tag.parent.parent

    tag = table.find(text=re.compile(r'Release date'))
    date = tag.parent.parent.parent
    try:
        info["Month"] = date.find('ul').text
    except:
        info["Month"] = date.find('th').text
    
    tag = table.find(text=re.compile(r'Running time'))
    time = tag.parent.parent.parent

    
    info["Budget"] = budget.find('td').text
    info["Box Office"] = box.find('td').text
    
    info["Length"] = time.find('td').text

    return info
    
def get_wiki_link(input_id):
    link = 'https://imdb-api.com/en/API/Wikipedia/' + use_key + '/' + input_id
    data = requests.get(link)
    wiki_info = json.loads(data.text)

    wiki_html = wiki_info['url']

    return get_wiki(wiki_html)
    

#regex \b\w* (month)
#regex \d* million|\d* thousand (box office and budget)

def build_db(cur, conn):
    link = 'https://imdb-api.com/API/Top250Movies/' + use_key + '/'
    data = requests.get(link)
    movie_dict = json.loads(data.text)
    

    #cur.execute("SELECT MAX(Rank) FROM IMDB_data")
    #SELECT UNIQUE Rank 

    for i in movie_dict['items']:
        name = i['title']
        id = i['id']
        rank = i['rank']
        year = i['year']
        rating = i['imDbRating']

        
        cur.execute("""
        INSERT OR IGNORE INTO IMDB_data (Name, id, Rank, Year, Rating)
        VALUES (?,?,?,?,?)
        """,
        (name, id, rank, year, rating))

        conn.commit()
        
        wiki_values = get_wiki_link(id)

        date = wiki_values["Month"]
        budget = wiki_values["Budget"]
        box_office = wiki_values["Box Office"]
        length = wiki_values["Length"]

        
        cur.execute("""
        INSERT OR IGNORE INTO Wiki_data (Name, date, Budget, Box_office, Length)
        VALUES (?,?,?,?,?)
        """,
        (name, date, budget, box_office, length))
        
        conn.commit()
        
        #LIMIT 25


def main():
    cur, conn = setup_database('IMDB-data.db')
    setup_IMDB_table(cur, conn)
    setup_wiki_table(cur, conn)
   
    #repeat 10 times, to get all 250 datapoints
    build_db(cur, conn)

    print("all done!!!\n")
    
    """"
    wiki_data = get_wiki()
    """
main()
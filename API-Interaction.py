import sqlite3
import json
import os
import requests
import bs4
import re
import locale

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

def get_wiki(film_id):

    wiki_html = "https://www.boxofficemojo.com/title/" + film_id
    url = wiki_html
    resp = requests.get(url)
    soup = bs4.BeautifulSoup(resp.content, "html.parser")
    table = soup.find('div', class_ = "a-section a-spacing-none mojo-summary-values mojo-hidden-from-mobile")
    
    info = {}

    try:
        tag = table.find(text=re.compile(r'Budget'))
        budget = tag.parent.parent
        budget_text = budget.find('span', class_ = "money").text
    except:
        budget_text = "00"

    try:
        #tag = soup.find(text=re.compile(r'Original Release'))
        tag = soup.find('tr', class_ = 'mojo-revenue-source-theatrical')
        box = tag
        box_text = box.find('span', class_ = "money").text
    except:
        box_text = "00"

    try:
        tag = table.find(text=re.compile(r'Earliest Release Date'))
        date = tag.parent.parent
        month_1 = date.find_all('span')
        month_text = re.search("span>(\w+)", str(month_1[1]))[1]
    except:
        month_text = "NA"


    tag = table.find(text=re.compile(r'Running Time'))
    time = tag.parent.parent    
    time_1 = time.find_all('span')
    time_text = re.search(("span>(.+)</"), str(time_1[1]))[0]
    

    info["Month"] = re.search('\w+', month_text)[0]
    info["Budget"] = clean_num(budget_text[1:])
    info["Box Office"] = clean_num(box_text[1:])
    info["Length"] = convert_time(time_text)  #re.search('\', time_text)[0]

    return info
    
def clean_num(number):
    locale.setlocale(locale.LC_ALL, "")
    return locale.atoi(number)

def convert_time(time):
    try:
        hours = re.search('(\d+) hr', time)[1]
    except:
        hours = '0'
    try:
        mins = re.search('(\d+) min', time)[1]
    except:
        mins = '0'
    hournum = int(str(hours))* 60
    total = hournum + int(str(mins))
    return total
    

#regex \b\w* (month)
#regex (\d*) (million)|(\d*) (thousand) (box office and budget)

def build_db(cur, conn):
    link = 'https://imdb-api.com/API/Top250Movies/' + use_key + '/'
    data = requests.get(link)
    movie_dict = json.loads(data.text)
    
    try:
        cur.execute("SELECT MAX(Rank) FROM IMDB_data")
        max_rank = int(str(cur.fetchall()[0][0]))
    except:
        max_rank = 1

    for i in movie_dict['items']:

        name = i['title']
        id = i['id']
        rank = i['rank']
        year = i['year']
        rating = i['imDbRating']

        if int(rank) < int(max_rank):
            continue
        
        cur.execute("""
        INSERT OR IGNORE INTO IMDB_data (Name, id, Rank, Year, Rating)
        VALUES (?,?,?,?,?)
        """,
        (name, id, rank, year, rating))

        conn.commit()
        
        wiki_values = get_wiki(id)

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

        if int(rank) >= max_rank + 25:
            break
        print(rank)
        
        #LIMIT 25

def realtest():
    cur, conn = setup_database('IMDB-data.db')
    setup_IMDB_table(cur, conn)
    setup_wiki_table(cur, conn)
   
    #repeat 10 times, to get all 250 datapoints
    build_db(cur, conn)

def faketest():
    print(get_wiki("tt0325980"))



def main():
    realtest()
    #faketest()
main()
# box office by month 
# budget to box office 
# budget per minute
#

import sqlite3
import os
import re
from collections import OrderedDict
import matplotlib.pyplot as plt
import numpy as np

def setup_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def films_by_month(cur, conn):
    cur.execute('''
    SELECT COUNT(*), date 
    FROM Wiki_data 
    GROUP BY date
    ''')
    conn.commit()
    data = cur.fetchall()

    months_dict={}

    for i in data:
        if i[1] != 'NA':
            months_dict[i[1]] = i[0]

    months = ['January','February','March','April','May','June','July','August','September','October','November','December']    
    months_ordered_dict = dict(OrderedDict(sorted(months_dict.items(),key =lambda x:months.index(x[0]))))

    
    plt.bar(list(months_ordered_dict.keys()),list(months_ordered_dict.values()), color = ['darkred', 'darkorchid', 'lightskyblue', 'white', 'green', 'plum', 'red', 'lightgreen', 'navy', 'deeppink', 'yellow', 'blue'], edgecolor = 'black')
    plt.xticks(rotation=70) 
    plt.xlabel('Month') 
    plt.ylabel('Number of Movies in Top 250') 
    plt.title('Top 250 Movies By Month') 
    plt.show()

def rank_and_budget(cur, conn):
    cur.execute('''
    SELECT IMDB_data.Rank, Wiki_data.Budget, IMDB_data.Name 
    FROM Wiki_data 
    JOIN IMDB_data
    ON Wiki_data.Name = IMDB_data.Name
    ''')
    conn.commit()
    data = cur.fetchall()
    data_dict = {}

    for i in data:
        budget = int(i[1])
        if budget !=0:
            data_dict[budget]= i[0]

    plt.scatter(list(data_dict.keys()), list(data_dict.values()))
    plt.xticks(rotation=70) 
    plt.xlabel('Budget') 
    plt.ylabel('Rank') 
    plt.title('Top 250 Movies Rank Compared to Budget') 
    plt.show()


def main():
    cur, conn = setup_database('IMDB-data.db')
    #print(films_by_month(cur,conn))
    print(rank_and_budget(cur, conn))

main()
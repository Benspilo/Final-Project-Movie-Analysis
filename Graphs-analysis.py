#r

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

    x = np.array(list(data_dict.keys()))

    plt.scatter(list(data_dict.keys()), list(data_dict.values()), c = x, cmap = 'cividis', edgecolor = 'navy')
    plt.xticks(rotation=70) 
    plt.xlabel('Budget') 
    plt.ylabel('Rank') 
    plt.title('Top 250 Movies Rank Compared to Budget') 
    #plt.grid()
    plt.show()
"""
def budget_per_min_to_ratings(cur, conn):
    cur.execute('''
    SELECT IMDB_data.Rank, Wiki_data.Budget, Wiki_data.Length 
    FROM Wiki_data 
    JOIN IMDB_data
    ON Wiki_data.Name = IMDB_data.Name
    ''')
    conn.commit()
    data=cur.fetchall()
    rank_dict = {}

    for i in data:
        budget = int(i[1])
        length = int(i[2])
        if budget != 0:
            budget_over_length = budget/length
            rank_dict[i[0]] = int(round(budget_over_length, 0))

    x = np.array(list(rank_dict.keys()))
    y= np.array(list(rank_dict.values()))

    r = np.sqrt(x ** 2 + y ** 2)  
    plt.scatter((rank_dict.keys()), rank_dict.values())
    m, b = np.polyfit(x, y, 1) 
    plt.plot(x, m*x+b)
    plt.xticks(rotation=70) 
    plt.xlabel('Rank') 
    plt.ylabel('Budget Per Minute') 
    plt.title('Rank of Films By Budget Per Minute') 
    plt.grid()
    plt.show()
    return r
"""

def budget_per_min_to_box(cur, conn):
    cur.execute('''
    SELECT Wiki_data.Box_office, Wiki_data.Budget, Wiki_data.Length 
    FROM Wiki_data 
    ''')
    conn.commit()
    data=cur.fetchall()
    box_dict ={}

    for i in data:
        budget = int(i[1])
        length = int(i[2])
        box = int(i[0])
        if (box != 0) and (budget != 0):
            budget_over_length = budget/length
            box_dict[box] = int(round(budget_over_length, 0))

    x = np.array(list(box_dict.values()))
    y= np.array(list(box_dict.keys()))

    plt.scatter((box_dict.values()), box_dict.keys(), c= x, cmap = 'coolwarm', edgecolor = 'black')
    m, b = np.polyfit(x, y, 1) 
    plt.plot(x, m*x+b)
    plt.xticks(rotation=70) 
    plt.xlabel('Budget Per Minute') 
    plt.ylabel('Box Office') 
    plt.title('Budget Per Minute of Films By Box Office') 
    #plt.grid()
    plt.show()

def rating_to_box(cur, conn):
    cur.execute('''
    SELECT Wiki_data.Box_office, IMDB_data.Rating
    FROM Wiki_data 
    JOIN IMDB_data
    ON Wiki_data.Name = IMDB_data.Name
    ''')
    conn.commit()
    data=cur.fetchall()
    
    data_dict = {}
    color_dict = {}

    for i in data:
        box = int(i[0])
        rating = i[1]
        if box != 0:
            data_dict[box] = rating
            color_dict[rating] = 0

    x = np.array(list(data_dict.keys()))
    y= np.array(list(data_dict.values()))
    z= list(color_dict.keys())

    plt.scatter((data_dict.keys()), data_dict.values(), c=y)
    m, b = np.polyfit(x, y, 1) 
    plt.xticks(rotation=70) 
    plt.xlabel('Box Office') 
    plt.ylabel('Ratting') 
    plt.title('Box Office By Individual Rating')
    plt.grid(True) 
    plt.show()

 



def main():
    cur, conn = setup_database('IMDB-data.db')
    print(films_by_month(cur,conn))
    print(rank_and_budget(cur, conn))
    #print(budget_per_min_to_ratings(cur,conn))
    print(budget_per_min_to_box(cur,conn))
    print(rating_to_box(cur, conn))

main()
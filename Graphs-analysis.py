# box office by month 
# budget to box office 
# budget per minute
#

import sqlite3
import os
import re

def setup_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def box_by_month(cur, conn):
    cur.execute('''
    SELECT Wiki_data.box_office, Wiki_data.release_date 
    FROM Wiki_data 
    GROUP BY Wiki_data.release_date
    ''')


def main():
    cur, conn = setup_database('IMDB-data.db')
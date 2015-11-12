import pymysql
from collections import defaultdict
import pickle

def connect():
    connection = pymysql.connect(host='localhost', user='nina',
                                 password='nina_secure', db='urltracker',
                                 charset='utf8', use_unicode=True,
                                 autocommit = True   )
    return connection.cursor()

def closeconnection(cur):
    conn = cur.connection
    cur.close()
    conn.close()


def get_langs():
    cur = connect()
    sql_lang = "SELECT lang FROM events \
                WHERE ip is not null and domain is not null \
                      and lang is not null"
    cur.execute(sql_lang)
    print("lang " , cur.rowcount)

    dict = defaultdict(int)
    for row in cur:
        lang = row[0][0:2]
        dict[lang] += 1

    return dict
    

if __name__ == "__main__":
    langs = get_langs()
    pickle.dump(langs, open('../databases/totallangcount', 'wb'))
    # langs = pickle.load(open('../databases/totallangcount', 'rb'))
    print("Languages: ", len(langs))
    print("Englisch: ", langs['en'])
    print("Deutsch: ", langs['de'])
    print("French: ", langs['fr'])
    print("Italian: ", langs['it'])

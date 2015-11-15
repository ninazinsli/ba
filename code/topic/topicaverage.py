import pymysql
from collections import defaultdict
import pickle
import gc

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

def get_topics(loctopperc):
    dict = {}
    for t in loctopperc:
        for (to,p) in loctopperc[t]:
            dict[to] = 0
    print("topics finished")
    return dict

def average(loctopperc, topics):
    noloc = len(loctopperc)
    for topic in topics:
        avg = 0
        for t in loctopperc:
            for (to,p) in loctopperc[t]:
                if to == topic:
                    avg += p
        avg /= noloc
        topics[topic] = avg

def main():
    loctopperc = pickle.load(
        open('../../databases/dict[locid]list:(topic,perc)',
                                'rb'))
    topics = get_topics(loctopperc)
    average(loctopperc, topics)

    pickle.dump(topics, open('../../databases/dict[topic]avg', 'wb'))
    topics = pickle.load(open('../../databases/dict[topic]avg', 'rb'))

if __name__ == "__main__":
    main()

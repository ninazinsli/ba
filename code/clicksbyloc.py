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


def dict_iploc():
    cur = connect()
    sqlloc = "SELECT ip, locid FROM iploc  \
              WHERE locid <> 44"
    cur.execute(sqlloc)
    dict = {}
    for row in cur:
        dict[row[0]] = row[1]
    closeconnection(cur)
    print("Iploc dict done")
    return dict

def list_events():
    gc.disable()
    cur = connect()
    list = []
    sql_events = "SELECT ip, domain FROM events_md5 limit 50"
    cur.execute(sql_events)
    print("events selected")
    for row in cur:
        ip = row[0]
        domain = row[1]
        list.append((ip, domain))
    
    closeconnection(cur)
    print("Events list done")
    gc.enable()
    return list


def main():
    #iploc = dict_iploc()
    #pickle.dump(iploc, open("iploc_dict", "wb"))
    iploc = pickle.load(open("iploc_dict", "rb"))
    #events = list_events()
    #pickle.dump(events, open("events_list.txt", "wb"))
    events = pickle.load(open("events_list.txt", "rb"))
    print("loading done")
    
    
    # Save clicksperloc to dict
    dict = {}
    for event in events:
        ip = event[0]
        if ip in iploc:
            locid = iploc[ip]
            if locid in dict:
                dict[locid] += 1
            else:
                dict[locid] = 1

    pickle.dump(dict, open("clicksperloc.txt", "wb"))
    print("dict done")

    # Write dict to database
    cur = connect()
    for loc in dict.keys():
        count= dict[loc]
        sqlinsert = "INSERT INTO clicksperloc (locid, count)\
                     VALUES (\'%s\', \'%s\')" %(loc, count)
        cur.execute(sqlinsert)
        
            
    closeconnection(cur)

if __name__ == "__main__":
    main()

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

def dict_sites():
    cur = connect()
    sqlsites = "SELECT name, categorystring FROM sites \
                WHERE name is not null and categorystring is not null"
    cur.execute(sqlsites)
    dict = defaultdict(list)
    for row in cur:
        domain = row[0]
        cat = row[1]
        if dict[domain]:
            dict[domain].append(cat)
        else:
            dict[row[0]] = [cat]
    closeconnection(cur)
    print("Sites dict done")
    return dict

def list_events():
    gc.disable()
    cur = connect()
    list = []
    sql_events = "SELECT ip, domain FROM events_md5"
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
    #pickle.dump(iploc, open("../databases/dict[ip]locid", "wb"))
    iploc = pickle.load(open("../databases/dict[ip]locid", "rb"))
    sites = dict_sites()
    events = list_events()
    #pickle.dump(events, open("../databases/list[ip,domain]", "wb"))
    #print("Events saved")
    events = pickle.load(open("../databases/list[ip,domain]", "rb"))
    #print(eventsl)

    # Save events to dict
    dict = {}
    for event in events:
        ip = event[0]
        domain = event[1]
        
        if ip in iploc and domain in sites:
            locid = iploc[ip]
            cat = sites[domain]
            for c in cat:
                if (locid,c) in dict:
                    dict[(locid, c)] += 1
                else:
                    dict[(locid, c)] = 1

    pickle.dump(dict, open("../databases/dict[(locid,cat)]count", "wb"))
    print("dict done")

    # Write dict to database
    cur = connect()
    for d in dict.keys():
        loc = d[0]
        cat = d[1]
        count= dict[d]
        sqlinsert = "INSERT INTO loccategory (locid, categoryid, count)\
                     VALUES (\'%s\', \'%s\', \'%s\')" %(loc, cat, count)
        cur.execute(sqlinsert)
        
            
    closeconnection(cur)

if __name__ == "__main__":
    main()

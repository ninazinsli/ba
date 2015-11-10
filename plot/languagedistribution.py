import pymysql
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
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

def get_iplang():
    cur = connect()
    dict = {}
    sql_iplang = "SELECT lang, ip \
                  FROM events \
                  WHERE ip is not null and domain is not null \
                         and lang is not null"
    cur.execute(sql_iplang)
    print("selected ", cur.rowcount)
    for row in cur:
        langs = row[0].split(";")[0]
        ip = row[1]
        if (ip, langs) in dict:
            dict[(ip, langs)] += 1
        else:
            dict[(ip, langs)] = 1
    print("iplang done ", len(dict))
    closeconnection(cur)
    return dict

def get_langloc(iplang):
    dict = {}
    iploc = pickle.load(open("../databases/dict[ip]locid", "rb"))
    for (ip, langs) in iplang:
        if ip in iploc:
            locid = iploc[ip]
            dict[(locid, langs)] = iplang[(ip, langs)]

    print("langloc ", len(dict))
    return dict

def get_langdistribution(langloc, l):
    dict = {}
    loco = pickle.load(open("../databases/dict[locid]lat,lon", "rb"))
    for (locid,langs) in langloc:
        if l in langs and locid in loco:
            co = loco[locid]
            if co in dict:
                dict[co] += 1
            else:
                dict[co] = 1
    print("lang dist ", len(dict))
    return dict
    
if __name__ == "__main__":
    # Read values from databases
    #iplang = get_iplang()
    #pickle.dump(iplang, open("../databases/dict[(ip,langs)]count", "wb"))
    #iplang = pickle.load(open("../databases/dict[(ip,langs)]count", "rb"))
    #print("iplang saved")
    
    #langloc = get_langloc(iplang)
    #pickle.dump(langloc, open("../databases/dict[(locid,langs)]count", "wb"))

    langloc = pickle.load(open("../databases/dict[(locid,langs)]count", "rb"))

    #print("langloc saved")

    dist = get_langdistribution(langloc, "en")
    #print("dist done ", len(dist))
    
    # Make map
    width = 400000
    height = 300000
    res = 'f'
    proj = 'tmerc'
    lon = 8.25
    lat = 46.75
    
    ch_map = Basemap(projection=proj, height = height, width = width,
                     lat_0=lat, lon_0=lon,
                     resolution=res, area_thresh = 1000.0)
    #ch_map.drawcoastlines()
    #ch_map.drawstates()
    ch_map.drawcountries(linewidth = 1.5)

    print("map done")

    min_marker_size = 1E-1
    
    for c in dist:
        x,y = ch_map(c[1], c[0])
        msize = (dist[c] * min_marker_size)
        ch_map.plot(x, y, 'ro', markersize=msize)

        
    plt.savefig('langenglish.png')
    plt.show()

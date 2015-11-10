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

def get_loccoord():
    cur = connect()
    dict = {}
    sql_loccoord = "SELECT locid, latitude, longitude \
                    FROM geolite_loc_coord"
    cur.execute(sql_loccoord)
    for row in cur:
        dict[row[0]] = (row[1], row[2])
    return dict

def clicksperloc(loco):
    dict = {}
    cur = connect()
    sql_cpl = "SELECT locid, count FROM clicksperloc"
    cur.execute(sql_cpl)
    for row in cur:
        locid = row[0]
        count = row[1]
        if locid != 44 and locid in loco:
            lat = loco[locid][0]
            lon = loco[locid][1]
            if lat != 0:
                dict[(lat,lon)] = count
    return dict
    
if __name__ == "__main__":
    # Read values from databases
    #loccoord = get_loccoord()
    #pickle.dump(loccoord, open("loccoord_dict", "wb"))
    loccoord = pickle.load(open("../databases/dict[(locid,langs)]count", "rb"))
    print("loco saved")
    
    #clicks = clicksperloc(loccoord)
    #pickle.dump(clicks, open("clicksperloccoord_dict", "wb"))
    clicks = pickle.load(open("../databases/clicksperloccoord_dict", "rb"))
    print("clicks saved")
    
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

    min_marker_size = 2*1E-4
    
    for c in clicks:
        x,y = ch_map(c[1], c[0])
        msize = (clicks[c] * min_marker_size)
        ch_map.plot(x, y, 'ro', markersize=msize)

        
    plt.savefig('clickspercoord.png')
    plt.show()

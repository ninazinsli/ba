import pymysql
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import pickle
from collections import defaultdict


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

def get_topicdistribution(topics):
    loccoord = pickle.load(open("../databases/dict[locid]lat,lon", "rb"))
    clicks = defaultdict(int)
    for t in topics.keys():
        if t in loccoord:
            if topic in list(zip(*topics[t]))[0]:
                clicks[loccoord[t]] += 1

    print("total number of locations with topic: ", len(clicks))
    return clicks

    
if __name__ == "__main__":

    # Topic whose distribution is plotted
    topic = 48
    
    # Read values from databases
    topicsabs = pickle.load(open("../databases/dict[locid]list:(topic,count)",
                              "rb"))
    topicsrel = pickle.load(open("../databases/dict[locid]list:(topic,perc)",
                                 "rb"))


    # Get absolute or relative distribution
    clicks = get_topicdistribution(topicsrel)
                
    
    # Make map
    width = 400000
    height = 300000
    res = 'l'
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

    min_marker_size = 5
    
    for c in clicks:
        x,y = ch_map(c[1], c[0])
        msize = (clicks[c] * min_marker_size)
        ch_map.plot(x, y, 'ro', markersize=msize)

        
    #plt.savefig('clickspercoord.png')
    plt.show()

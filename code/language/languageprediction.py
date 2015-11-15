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


def count_lang():
    loclang = pickle.load(open("../../databases/dict[(locid,lang)]count",
                               "rb"))
    it = defaultdict(int)
    fr = defaultdict(int)
    de = defaultdict(int)
    
    for (locid, lang) in loclang:
        if lang == 'de':
            de[locid] = loclang[(locid, lang)]
        elif lang == 'it':
            it[locid] = loclang[(locid, lang)]
        elif lang == 'fr':
            fr[locid] = loclang[(locid, lang)]

    mainlang = defaultdict()
    locids = pickle.load(open("../../databases/dict[locid]clicks", "rb"))

    for locid in locids:
        noit, nofr, node = it[locid], fr[locid], de[locid]
        if (noit == nofr and noit == node) or (noit == nofr and node < noit) or (noit == node and nofr < noit) or (nofr == node and noit < nofr):
            mainlang[locid] = 'no pref'
        elif (node > nofr) and (node > noit):
            mainlang[locid] = 'de'
        elif (nofr > node) and (nofr > noit):
            mainlang[locid] = 'fr'
        else:
            mainlang[locid] = 'it'

    return mainlang
        
def find_false(mainlang):
    stat = pickle.load(open("../../databases/stat[code]lang", "rb"))
    codes = pickle.load(open("../../databases/dict[locid]code", "rb"))

    counter = 0
    dict = defaultdict()
    for locid in mainlang:
        if mainlang[locid] == 'no pref':
            counter += 1
        elif locid in codes and codes[locid] in stat:
            if not stat[codes[locid]].lower().startswith(mainlang[locid]):
                dict[locid] = (mainlang[locid],  stat[codes[locid]])
    print("No preference: ", counter)
    return dict
    
    
if __name__ == "__main__":

    main_lang = count_lang()
    print("Locations: ", len(main_lang))

    wrong = find_false(main_lang)
    print("Wrongly predicted: ", len(wrong))

    loccoord = pickle.load(open('../../databases/dict[locid]lat,lon', 'rb'))
    
    wrongge = defaultdict()
    wrongfr = defaultdict()
    wrongit = defaultdict()
    for locid in wrong:
        false, right = wrong[locid]
        if false == "de":
            print("Predicted %s instead of %s in %s \n" %(false,right,locid))
            if locid in loccoord:
                wrongge[locid] = loccoord[locid]
                lat,lon = tuple(loccoord[locid])
                if float(lat) > 46.9167 and float(lon) > 7.4667:
                    print("Predicted %s instead of %s in %s" %(false,right,locid))
        if false == "fr":
            if locid in loccoord:
                wrongfr[locid] = loccoord[locid]
        if false == "it":
            if locid in loccoord:
                wrongge[locid] = loccoord[locid]
                
    dict = wrongge
    print("Total wrong: " , len(dict))
    
    # # Make map
    # width = 400000
    # height = 300000
    # res = 'l'
    # proj = 'tmerc'
    # lon = 8.25
    # lat = 46.75
    
    # ch_map = Basemap(projection=proj, height = height, width = width,
    #                  lat_0=lat, lon_0=lon,
    #                  resolution=res, area_thresh = 1000.0)
    # #ch_map.drawcoastlines()
    # #ch_map.drawstates()
    # ch_map.drawcountries(linewidth = 1.5)

    # print("map done")

    # min_marker_size = 0.5
    
    # for c in dict.values():
    #     x,y = ch_map(c[1], c[0])
    #     #msize = (dict[c] * min_marker_size)
    #     msize = 1
    #     ch_map.plot(x, y, 'ro', markersize=msize)

        
    # #plt.savefig('langother1.png')
    # plt.show()
    

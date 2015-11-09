import pymysql
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

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


if __name__ == "__main__":
    width = 400000
    height = 300000
    res = 'f'
    proj = 'tmerc'
    lon = 8.25
    lat = 46.75
    
    ch_map = Basemap(projection=proj, height = height, width = width,
                     lat_0=lat, lon_0=lon,
                     resolution=res)
    #ch_map.drawcoastlines()
    #ch_map.drawstates()
    ch_map.drawcountries(linewidth = 1.5)
    
    plt.show()

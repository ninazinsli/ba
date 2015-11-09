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

    my_map = Basemap(projection='ortho', lat_0=50, lon_0=0,
              resolution='l', area_thresh=1000.0)
    my_map.drawcoastlines()
    my_map.drawstates()
    my_map.drawcountries()
    
    plt.show()

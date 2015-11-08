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



def main():
    cur = connect()
    cur2 = connect()
    cur3 = connect()
    sql_clicksperloc = "SELECT locid FROM clicksperloc"
    cur.execute(sql_clicksperloc)
    print("selected")

    for row in cur:
        locid = row[0]
        sql_city = "SELECT city FROM geolite_locations \
                    WHERE locid = \'%s\'" %locid
        cur2.execute(sql_city)

        sql_update = "UPDATE clicksperloc SET city = \'%s\' \
                      WHERE locid = \'%s\'" %(cur2.fetchone()[0], locid)
        cur3.execute(sql_update)
            
    closeconnection(cur)
    closeconnection(cur2)
    closeconnection(cur3)
    

if __name__ == "__main__":
    main()

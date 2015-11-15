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

    sql_loccode = "SELECT locid, code FROM location \
                   WHERE code is not null"
    cur.execute(sql_loccode)
    print("selected")

    dictloc = defaultdict(int)
    dictcode = defaultdict(list)
    for row in cur:
        locid = row[0]
        code = row[1]
        dictloc[locid] = code
        dictcode[code].append(locid)

    pickle.dump(dictloc, open('../databases/dict[locid]code', 'wb'))
    pickle.dump(dictcode, open('../databases/dd[code]locidlist', 'wb'))

if __name__ == "__main__":
    main()

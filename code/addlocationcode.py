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

    #ziptocode = pickle.load(open("../databases/ziptocode", "rb"))
    namecode = pickle.load(open("../databases/namecode", "rb"))

    codename = defaultdict()
    for k in namecode.keys():
        
        codename[namecode[k][0]] = k

            
    sql_city = "SELECT city FROM location where code is null limit 20"
    cur.execute(sql_city)
    print("%s cities selected" %cur.rowcount)
    

    for row in cur:
        name = row[0]
        if name in codename:
            code = codename[name]
            sql_update = "UPDATE location SET code = \'%s\' \
                          WHERE city = \'%s\'" %(code, name)
            cur2.execute(sql_update)
        else:
            print(name)

            
    closeconnection(cur)
    closeconnection(cur2)
    

if __name__ == "__main__":
    main()

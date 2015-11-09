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

    ziptocode = pickle.load(open("../databases/ziptocode", "rb"))
    
    sql_zip = "SELECT distinct(zip) FROM location"
    cur.execute(sql_zip)
    print("%s zips selected" %cur.rowcount)

    
    more = 0
    for row in cur:
        zip = row[0]
        if zip in ziptocode:
            codes = ziptocode[zip]
            if len(codes) == 1:
                code = codes[0]
            else:
                #print("more than one ", zip)
                #print(codes)
                more += 1

                sql_update = "UPDATE location SET code = \'%s\' \
                              WHERE zip = \'%s\'" %(code, zip)
                #cur2.execute(sql_update)


    print("more ", more)
            
    closeconnection(cur)
    closeconnection(cur2)
    

if __name__ == "__main__":
    main()

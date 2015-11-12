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


def transform(city):
    city.replace('(', '')
    city.replace(')', '')
    city = city.lower()
    city.replace('ue','u')
    city.replace('ae','a')
    city.replace('oe','o')
    city.replace('ue','u')
    city.replace('ä','a')
    city.replace('ö','o')
    city.replace('ü','u')
    city.replace('saint', 'st.')

    return city
    

def main():
    cur = connect()
    cur2 = connect()

    #ziptocode = pickle.load(open("../databases/dd[zip]codelist", "rb"))
    namecode = pickle.load(open("../databases/dd[code]citylist", "rb"))

    codename = defaultdict()
    for k in namecode.keys():
        city = transform(namecode[k][0])
        codename[city] = k
            

            
    sql_city = "SELECT city FROM location where code is null"
    cur.execute(sql_city)
    print("%s cities selected" %cur.rowcount)
    

    for row in cur:
        name = transform(row[0])
        if name in codename:
            code = codename[name]
            sql_update = "UPDATE location SET code = \'%s\' \
                          WHERE city = \'%s\'" %(code, row[0])
            #print(code, name)
            cur2.execute(sql_update)
        #else:
            #print(name)

            
    closeconnection(cur)
    closeconnection(cur2)
    

if __name__ == "__main__":
    main()

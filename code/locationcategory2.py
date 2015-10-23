import pymysql

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

    sqlloc = "SELECT ip, locid FROM iploc  \
              WHERE locid <> 44 limit 50"
    cur.execute(sqlloc)
    print(cur.rowcount, "locations and ip selected")

    dict = {}
    for res in cur.fetchall():
        print("start res")
        ip = res[0]
        locid = res[1]
        sqlcat = "SELECT s.categorystring \
                  FROM (SELECT md5domain FROM events_md5 \
                        WHERE ip = '%s') e \
                  INNER JOIN \
                  sites s \
                  ON (e.md5domain = s.md5name COLLATE utf8_unicode_ci)" %ip
        print(sqlcat)
        cur2.execute(sqlcat)
        print("Executed query")
        for s in cur2.fetchall():
            cat = s[0]
            if cat:
                #print("cat ", cat)
                if dict.get((locid, cat)):
                    dict[(locid, cat)] += 1
                else:
                    dict[(locid, cat)] = 1

        #print("next res")
        
    #print("Dict: ", dict)
    print("Dict done")
    
    for d in dict.keys():
        loc = d[0]
        cat = d[1]
        count= dict[d]
        sqlinsert = "INSERT INTO loccategory (locid, categoryid, count)\
                     VALUES (\'%s\', \'%s\', \'%s\')" %(loc, cat, count)
        cur.execute(sqlinsert)
        
            
    closeconnection(cur)
    closeconnection(cur2)


if __name__ == '__main__':
    main()

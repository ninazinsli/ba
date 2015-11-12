import pymysql

# too slow

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
    cur4 = connect()

    sqlloc = "SELECT ip, locid FROM iplocations  \
              WHERE locid not like '44' \
              Limit 50"
    cur.execute(sqlloc)
    print("Locations and ip selected")

    dict = {}
    for res in cur.fetchall():
        ip = res[0]
        locid = res[1]
        sql1 = "SELECT domain FROM events WHERE ip like \'%s\'" %ip
        cur2.execute(sql1)
        print("domain")
        for dom in cur2.fetchall():
            sql2 = "SELECT categorystring FROM sites \
                    WHERE name like \'%s\' COLLATE utf8_unicode_ci" %dom[0]
            cur3.execute(sql2)
            print("categorystring")
            for catid in cur3.fetchall():
                sql3 = "SELECT categories FROM categorystrings \
                        WHERE id like \'%s\'" %catid[0]
                cur4.execute(sql3)
                print("categories")
                cat = cur4.fetchone()[0]
                if dict.get((locid, cat)):
                    dict[(locid, cat)] += 1
                else:
                    dict[(locid, cat)] = 1

    print("Dict: ", dict)

    for d in dict.keys():
        loc = d[0]
        cat = d[1]
        count= dict[d]
        sqlinsert = "INSERT INTO loccategory (locid, category, count)\
                     VALUES (\'%s\', \'%s\', \'%s\')" %(loc, cat, count)
        #cur.execute(sqlinsert)
        
            
    closeconnection(cur)
    closeconnection(cur2)
    closeconnection(cur3)
    closeconnection(cur4)

    
if __name__ == '__main__':
    main()

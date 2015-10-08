import pymysql

def connect():
    connection = pymysql.connect(host='localhost', user='nina',
                                 password='nina_secure', db='urltracker',
                                 autocommit = True   )
    return connection.cursor()

def closeconnection(cur):
    conn = cur.connection
    cur.close()
    conn.close()


def main():
    cur = connect()
 
    sqluserip = "SELECT user, ip from events \
                 WHERE user is not null and ip is not null"

    cur.execute(sqluserip)

    useripset = set([])
    for res in cur.fetchall():
        useripset.add(res)

    #print("set ", useripset)

    for s in useripset:
        user = s[0]
        ip = s[1]
        if not ',' in ip and not '.com' in ip:
            sql = "INSERT INTO userip VALUES(\'%s\', \'%s\')" %(user, ip)
            cur.execute(sql)
        if ',' in ip:
            splitip = ip.split(',')
            sql1 = "INSERT INTO userip VALUES(\'%s\', \'%s\')" %(user, splitip[0])
            sql2 = "INSERT INTO userip VALUES(\'%s\', \'%s\')" %(user, splitip[1])
            cur.execute(sql1)
            cur.execute(sql2)        
            
    closeconnection(cur)


if __name__ == '__main__':
    main()

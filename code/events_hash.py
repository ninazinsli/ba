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

    sqlloc = "SELECT domain, ip FROM events  \
              WHERE domain is not null and ip is not null"
    cur.execute(sqlloc)
    print(cur.rowcount, "domains and ip selected")

    for res in cur.fetchall():
        ip = res[1]
        domain = res[0]
        sqlinsert = "INSERT INTO events_md5 (ip, domain, md5domain)\
                     VALUES (\'%s\', \'%s\', MD5(\'%s\'))" %(ip, domain, domain)
        #print(sqlinsert)
        cur.execute(sqlinsert)
        
            
    closeconnection(cur)
    closeconnection(cur2)


if __name__ == '__main__':
    main()

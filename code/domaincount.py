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
 
    sqldomain = "SELECT domain from events WHERE domain is not null"
    cur.execute(sqldomain)
    print("Domains selected")

    domaindict = {}
    for res in cur.fetchall():
        domain = res[0]
        if domaindict.get(domain):
            domaindict[domain] += 1
        else:
            domaindict[domain] = 1

    print("Domains counted")

    for domain in domaindict.keys():
        count = domaindict[domain]
        sqlcheck = "SELECT * FROM sites WHERE name like \'%s\'" %domain
        cur.execute(sqlcheck)
        if cur.fetchone():
            sqlinsert = "UPDATE sites \
                         SET count = \'%s\' \
                         WHERE name =\'%s\'" %(count, domain)
        else:
            sqlinsert = "INSERT INTO sites (name, count) \
                         values(\'%s\', \'%s\')" %(domain, count)
            
        cur.execute(sqlinsert)
        
            
    closeconnection(cur)


if __name__ == '__main__':
    main()

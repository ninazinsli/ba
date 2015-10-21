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

    sqlsites = "SELECT categorystring, count FROM sites \
                WHERE categorystring is not null \
                ORDER BY categorystring"
    cur.execute(sqlsites)
    print("Sites selected")

    cat = 6  # because we know first category is 'no category' 
    counter = 0
    for res in cur.fetchall():
        category = res[0]
        count = res[1]
        if cat == category:
            counter += count
        else:
            sqlinsert = "UPDATE categorystrings \
                         SET count = \'%s\' \
                         WHERE id =\'%s\'" %(counter, cat)
            cur2.execute(sqlinsert)
            cat = category
            counter = count

    # We still have to update the last category        
    sqlinsertlast = "UPDATE categorystrings \
                     SET count = \'%s\' \
                     WHERE id =\'%s\'" %(counter, cat)
    cur2.execute(sqlinsertlast)
        
            
    closeconnection(cur)
    closeconnection(cur2)


if __name__ == '__main__':
    main()

import pymysql
import csv

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

    f = open('../../geolite/GeoLiteCity-Blocks.csv', 'rt')
    reader = csv.reader(f, delimiter = ',')

    #skip header
    next(reader, None)
    next(reader, None)
    
    for row in reader:
        fromip = row[0]
        toip = row[1]
        locid = row[2]

        sql = "INSERT INTO geolite_blocks values(\'%s\', \'%s\', \'%s\')" %(fromip, toip, locid)
        #import pdb; pdb.set_trace()
        cur.execute(sql)
    
    f.close()
    
    closeconnection(cur)


if __name__ == '__main__':
    main()

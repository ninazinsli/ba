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

    f = open('../../geolite/GeoLiteCity-Location.csv', 'rt', encoding ="ISO-8859-1")
    reader = csv.reader(f, delimiter = ',')

    #skip header
    next(reader, None)
    next(reader, None)
    
    for row in reader:
        country = row[1]
        if country == 'CH':
            locid = row[0]
            city = row[3]
            zip = row[4]

            if ('\'' in city):
                city = city.replace('\'', ' ')
                
            sql = "INSERT INTO geolite_locations values(\'%s\', \'%s\', \'%s\')" %(locid, city, zip)
            #import pdb; pdb.set_trace()
            #print(sql)
            cur.execute(sql)
    
    f.close()
    
    closeconnection(cur)


if __name__ == '__main__':
    main()

import pymysql
import sys
import struct
import socket

def connect():
    connection = pymysql.connect(host='localhost', user='nina',
                                 password='nina_secure', db='urltracker',
                                 autocommit = True   )
    return connection.cursor()

def closeconnection(cur):
    conn = cur.connection
    cur.close()
    conn.close()

def iptoint(addr):
    try: 
        ip = struct.unpack("!I", socket.inet_aton(addr))[0]
    except:
        print("ERROR ", addr)
        ip = 0
    return ip

def intoip(addr):                                                             
    try:
        ip = socket.inet_ntoa(struct.pack("!I", addr))
    except:
        ip = 0
    return ip

def main():
    cur = connect()
    cur2 = connect()
    cur3 = connect()
 
    sqluserip = "SELECT ip from userip"

    cur.execute(sqluserip)


    for res in cur.fetchall():
        ip = res[0]
        ipint = iptoint(ip)
        
        sqllocid = "SELECT locid FROM geolite_blocks \
               WHERE \'%s\' > from_ip AND \'%s\' < to_ip" %(ipint, ipint)
        cur2.execute(sqllocid)
        for row in cur2.fetchall():
            locid = row[0]
            sql = "INSERT INTO iplocations \
                   VALUES(\'%s\', \'%s\', \'0\')"  % (ip, locid)
            cur3.execute(sql)
            
    closeconnection(cur)
    closeconnection(cur2)
    closeconnection(cur3)


if __name__ == '__main__':
    main()

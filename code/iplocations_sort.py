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

def inttoip(addr):                                                             
    try:
        ip = socket.inet_ntoa(struct.pack("!I", addr))
    except:
        ip = 0
    return ip

def main():
    cur = connect()
    cur2 = connect()
    cur3 = connect()
 
    sqluserip = "SELECT distinct(ip) from userip"

    cur.execute(sqluserip)
    print("ip selected")
    print("we found ", cur.rowcount, " ips")
    
    iplist = []
    for res in cur.fetchall():
        ip = res[0]
        ipint = iptoint(ip)
        iplist.append(ipint)

    iplist.sort()
    no = len(iplist)
    print("sorted")
    
    sqlranges = "SELECT * from geolite_blocks order by from_ip asc"
    cur2.execute(sqlranges)
    print("ranges selected")
    
    i = 0
    ip = iplist[i]
    for row in cur2.fetchall():
        from_ip = row[0]
        to_ip = row[1]
        locid = row[2]
        while ip < from_ip and i < no -1:
            i += 1
            ip = iplist[i]
        while ip >= from_ip and ip <= to_ip and i < no - 1:
            sql = "INSERT INTO iploc (ip, locid, geoname_id) \
                   VALUES(\'%s\', \'%s\', \'0\')"  % (inttoip(ip), locid)
            cur3.execute(sql)
            i += 1
            ip = iplist[i]
        
        
            
    closeconnection(cur)
    closeconnection(cur2)
    closeconnection(cur3)


if __name__ == '__main__':
    main()

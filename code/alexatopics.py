import pymysql
from bs4 import BeautifulSoup

def connect():
    connection = pymysql.connect(host='localhost', user='nina',
                                 password='nina_secure', db='urltracker',
                                 autocommit = True   )
    return connection.cursor()

def closeconnection(cur):
    conn = cur.connection
    cur.close()
    conn.close()

def sitename(site):
    title = ""    
    soup = BeautifulSoup(site, 'html.parser')
    title = soup.title.name.string
    title = title.split(" ")[0]
    try:
        title2 = site[site.find("<title>")+7:site.find("Site Overview")-1]
    print("Title soup: " + title)
    print("Title: " + title2)
    return title
    
def gettopic(site):
    topic = ""
    soup = BeautifulSoup(site, 'html.parser')
    print("Topic: " + topic)
    return topic
    
    
def addtopic(site, domains):
    cur = connect()
    cur2 = connect()
    sitename = sitename(site)
    # If information about one of our sites, get topic information
    if 'sitename' in domains:
        topic = gettopic(site)
        topicquery = "SELECT id FROM categoriystring \
                      WHERE categories like \'%s\'" %topic
        cur.execute(topicquery)
        # If topic already in database, add info about site to database
        # If not, first add topic to database
        if not cur.fetchone():
            topicinsert = "INSERT INTO categorystrings (categories) \
                           values(\'%s\')" %topic
            cur2.execute(topicinsert)
            topicquery = "SELECT id FROM categoriystring \
                          WHERE categories like \'%s\'" %topic
            cur.execute(topicquery)
        id = cur.fetchone()[0]
        insertsite = "INSERT INTO sites (name, categorystring) \
                      VALUES(\'%s\',\'%s\')" %(sitename, id)
        cur2.execute(insertsite)
        
        
    closeconnection(cur)
    closeconnection(cur2)
        
def main():
    cur = connect()

    # get all domains and safe them alphabetically ordered in a list
    sql_domain = "SELECT distinct(domain) FROM events \
                  WHERE domain is not null \
                  LIMIT 10"
    
    cur.execute(sql_domain)
    #domains = list(cur.fetchall())[6:] # first 6 elements are not usable
    domains = set(cur.fetchall())
    #print(domains)


    # Read alexa file info (one site at a time)
    alexafile = open("../../alexa/alexa-site-info")

    site = ""
    for line in alexafile:
        if "<html" in line:
            site = line
        elif "/html>" in line:
            site += line
            addtopic(site, domains)
        else:
            site += line

    
    closeconnection(cur)


if __name__ == "__main__":
    main()

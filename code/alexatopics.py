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

def get_sitename(site):
    site_name = ""    
    soup = BeautifulSoup(site, 'html.parser')
    site_name = soup.title.string
    #print("Site_name: " + site_name)
    site_name = site_name.split(" ")[0]
    #print("Sitename: " + site_name + ".")
    return site_name
    
def gettopic(site):
    topic = []
    soup = BeautifulSoup(site, 'html.parser')
    table = soup.find("table", {"id":"category_link_table"})
    for row in table.findAll("td"):
        t = ""
        for a in row.findAll('a'):            
            t += a.get_text()
            t += " / "
        topic.append(t)

    if "" in topic and len(topic) == 1:
        topic.append("no category")
        topic.remove("")
    print("Topic: " + str(topic))
    return topic
    
    
def addtopic(site, domains):
    cur = connect()
    cur2 = connect()
    sitename = get_sitename(site)
    # If information about one of our sites, get topic information
    if sitename in domains:
        #print("sitename found: " + sitename)
        topics = gettopic(site)
        for topic in topics:
            topicquery = "SELECT id FROM categorystrings \
                          WHERE categories like \'%s\'" %topic
            cur.execute(topicquery)
            # If topic already in database, add info about site to database
            # If not, first add topic to database
            if not cur.fetchone():
                topicinsert = "INSERT INTO categorystrings (categories) \
                               values(\'%s\')" %topic
                cur2.execute(topicinsert)
                topicquery = "SELECT id FROM categorystrings \
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
                  WHERE domain is not null"
    
    cur.execute(sql_domain)
    #domains = list(cur.fetchall())[6:] # first 6 elements are not usable
    domains = set(cur.fetchall())
    #print(domains)
    print("Domains geholt: " + len(domains))
    #domains.add("007james.com")

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

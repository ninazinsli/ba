import pymysql
from bs4 import BeautifulSoup

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
    #print("Topic: " + str(topic))
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
            try:
                cur.execute(topicquery)
            except:
                print("topicquery: " + topicquery)
                print("ERROR: " + sys.exc_info()[0])

                      
            # If topic already in database, add info about site to database
            # If not, first add topic to database
            id = cur.fetchone()
            if not id:
                topicinsert = "INSERT INTO categorystrings (categories) \
                               values(\'%s\')" %topic
                try:
                      cur2.execute(topicinsert)
                except:
                      print("topicinsert: " + topicinsert)
                      print("ERROR: " + sys.exc_info()[0])

                topicquery = "SELECT id FROM categorystrings \
                              WHERE categories like \'%s\'" %topic
                try:
                    cur.execute(topicquery)
                except:
                    print("topicquery: " + topicquery)
                    print("ERROR: " + sys.exc_info()[0])
                
                id = cur.fetchone()
                
            insertsite = "INSERT INTO sites (name, categorystring) \
                          VALUES(\'%s\',\'%s\')" %(sitename, id[0])

            try:
                cur2.execute(insertsite)
            except:
                print("insertsite: " + insertsite)
                print("ERROR: " + sys.exc_info()[0])
        

    closeconnection(cur)
    closeconnection(cur2)

    
        
def main():
    cur = connect()

    # get all domains and safe them alphabetically ordered in a list
    sql_domain = "SELECT distinct(domain) FROM events \
                  WHERE domain is not null"
#                  LIMIT 10"
    
    cur.execute(sql_domain)
    domains = set([])
    for d in cur.fetchall():
        domains.add(d[0])
    #print(domains)
    print("Domains geholt: " + str(len(domains)))

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

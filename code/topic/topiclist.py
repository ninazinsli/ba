import pymysql
from collections import defaultdict
import pickle
from operator import itemgetter

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

    locclicks = pickle.load(open("../../databases/dict[locid]clicks", "rb"))
    loccat = pickle.load(open("../../databases/dict[(locid,cat)]count", "rb"))

    # Add to topics dict[locid]: (category, clicks of this cat/ total clicks)
    topics = defaultdict(list)
    for (locid,cat) in loccat:
        #per = loccat[(locid,cat)] / locclicks[locid]
        topics[locid].append((cat,loccat[(locid,cat)]))
    print("1/3")
        
    # Sort topics list, s.t. most frequent are first
    for l in topics.keys():
        topics[l].sort(key = itemgetter(1), reverse = True)
    print("2/3")
        
    pickle.dump(topics, open('../../databases/dict[locid]list:(topic,count)', 'wb'))
    print("3/3")


    # topics = pickle.load(open('../../databases/dict[locid]list:(topic,perc)',
    #                           'rb'))

    # counter = 0
    # l = 0
    # maximum = 0
    # minimum = 200
    # for t in topics.keys():
    #     counter += 1
    #     length = len(topics[t])
    #     l += length
    #     if length < minimum:
    #         minimum = length
    #     if length > maximum:
    #         maximum = length
    # l /= counter

    # print("Number of locations: ", counter)
    # print("Average numbers of topics: ", l)
    # print("Maximum number of topics: ", maximum)
    # print("Minimum number of topics: ", minimum)
    
    
if __name__ == "__main__":
    main()

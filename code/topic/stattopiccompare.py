import xlrd
from collections import defaultdict
import pickle
from operator import itemgetter

# Return top 'topic_prop' % of topics, ordered by mean
# Return list[(topic, mean)]
def get_frequenttopics(topic_prop):
    dict = pickle.load(open('../../databases/dict[topic]avg', 'rb'))
    list = sorted(dict.items(), key = itemgetter(1), reverse=True)
    no = min(int(len(list) * topic_prop), len(list))
    return list[0:no]

# loc must be 'top' or 'bottom'
# Return 'prop' % at 'loc' of 'stat'
# Return list[(code, stat value)]
def get_statpart(stat, prop, loc):
    no = min(int(len(stat) * prop), len(stat))
    if loc == 'top':
        sortedlist = sorted(stat.items(), key=itemgetter(1), reverse=True)
        return sortedlist[0:no]
    else:
        sortedlist = sorted(stat.items(), key=itemgetter(1))
        l = len(sortedlist)
        return sortedlist[l-no:l]

def get_mean(stat, topic):
    cl = pickle.load(open('../../databases/dd[code]locidlist', 'rb'))
    ltp = pickle.load(open('../../databases/dict[locid]list:(topic,perc)','rb'))
    meancol = 0
    counter = 0
    for (code, value) in stat:
        if code in cl:
            for locid in cl[code]:
                if locid in ltp:
                    for (t,p) in ltp[locid]:
                        if t == topic:
                            counter += 1
                            meancol += p

    if counter > 0:
        print("Stats: " , len(stat))
        print("Counter: ", counter)
        return meancol / counter
    else:
        print("topic not found ", topic)
        return 0
    
        
def compare(statname, stat, stat_prop, topics, mean_bound):
    topstat = get_statpart(stat, stat_prop, 'top')
    bottomstat = get_statpart(stat, stat_prop, 'bottom')

    for (topic, mean) in topics:
        topmean = get_mean(topstat, topic)
        bottommean = get_mean(bottomstat, topic)

        # if topmean * (1+mean_bound) > mean:
        #     print("For statistic %s and topic %s:" %(statname, topic))
        #     print("Mean of top %s percent %s" %(stat_prop *100, topmean))
        #     print("Overall mean: %s" %mean)

        # if bottommean * (1+mean_bound) > mean:
        #     print("For statistic %s and topic %s:" %(statname, topic))
        #     print("Mean of bottom %s percent  %s" %(stat_prop*100, bottommean))
        #     print("Overall mean: %s" %mean)
            
    

                
if __name__ == '__main__':
    statname = "income"
    STAT = open('../../databases/stat[code]income', 'rb')
    stat_prop = 0.2  # % of top/bottom of statistics separately considered
    mean_bound = 1 # how much top/ bottom mean can differ from overall mean 

    topic_prop = 0.1 # % of most frequent topics considered
    topics = get_frequenttopics(topic_prop)
    
    compare(statname, pickle.load(STAT), stat_prop, topics, mean_bound)

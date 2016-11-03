from pyquery import PyQuery
import re

from settings import *
from process import *

# This method removes content within ()
# "eddard (the lord) stark" > "eddard stark"
def removeTags(s):
    while True:
        ob=s.find("(")
        cb=s.find(")",ob)
        if ob==-1 or cb==-1:
            break
        s=s[:ob]+s[cb+1:]
    return s

# This method extracts content within {}
# "eddard {the lord} stark{of winterfell} " > ["the lord", "of winterfell"]
# "nimish" > "nimish"
def extractTags(s):
    list = []
    while True:
        ob=s.find("{")
        cb=s.find("}",ob)
        if ob==-1 or cb==-1:
            break
        list.append(s[ob+1:cb])
        s=s[:ob]+s[cb+1:]

    return ([s] if list==[] else list)

# This method prepares the semantic graph (sub,pred,obj)
# { sub1: { pred1: [obj1,ob2],
#          pred2: [obj3, ob4]
#       },
#   sub2: { pred1: [obj1,ob2],
#          pred2: [obj3, ob4]
#       }
# }
def fetchInfoFromURL(url):

    d = PyQuery(url)         #cannot pass '' or ' '

    sub = url.split("/")[-1]
    graph[sub.lower()] = {'name': [sub.replace("_"," ")]}

    sub = sub.lower()        #uniqueue key
    predicates = d('#mw-content-text')('aside')('h3.pi-data-label')     #DOM ID, element, element.class
    objects = d('#mw-content-text')('aside')('div.pi-data-value')

    # print sub,"\n",predicates,"\n",objects
    # print len(predicates), len(objects)

    pattern_start = re.compile("^[,:\-\)}]")
    pattern_end = re.compile(".*( of| by|:|\(|{)$")

    for i in range(0,len(predicates)):
        pred = predicates.eq(i).text().strip().lower().replace(" ","_")
        all_objs =  objects.eq(i).contents()                                                    #['The Mountain That Rides', <Element br at 0x1015f0518>, 'The Mountain', <Element br at 0x1015f0fc8>, 'Tywin Lannister Mad Dog']
        # objs = filter(None, [PyQuery(e).text() for e in all_objs if e!=' ' and e!=''])        #need to use PyQuery(e) again because all_objs can contain a lxml object: <Element br at 0x1015f0518>

        objs = [PyQuery(t).text() for e in all_objs if e!=' ' and e!='' for t in PyQuery(e).contents() if t!=' ' and t!='']
        objs = [e for e in objs if e not in ['"',',','']]       # objs = filter(None,objs)

        # if pred == "children": print objs, "\n\n"
        for j in range(len(objs)-1,0,-1):
            if pattern_start.match(objs[j]):
                objs[j-1]+=objs[j]
                del objs[j]

        # if pred == "children": print objs, "\n\n"

        for j in range(len(objs) - 2, -1, -1):
            if pattern_end.match(objs[j]):
                objs[j] += (" "+objs[j+1])
                del objs[j+1]

        # if pred == "children": print objs, "\n\n"

        # Futher cleanup of obj values
        list_of_val= []
        for e in objs:
            list = extractTags(removeTags(e))
            for val in list:
                val = val.strip().lower().replace(" ", "_") if pred in link_predicates else val.strip()
                list_of_val.append(val)
        objs = filter(None,list_of_val)

        graph[sub][pred] = objs

    return 0

def main():

    f = open('/Users/nj/UFL/NLP/project/code/DataLinks.txt', 'r')
    for line in f:
        line = line[0:len(line)-1]
        print("Processing "+line)
        if (fetchInfoFromURL(line)):
            print("Failed processing " + line)
    f.close()
    f = open('/Users/nj/UFL/NLP/project/code/CollectedInfo.txt', 'w')       #use 'a', to append to previously saved file
    for (k, v) in graph.items():
        f.write("\n--------------------\n" + k + "\n--------------------\n")
        for (k2, v2) in v.items():
            # if k2 in link_predicates:
            f.write(str(k2) + ": " +str(v2) + "\n")
    f.close()


# --------------------------------------------------------------------------------------------------------------------------------------------------------
main()
print describe('Arya Stark')
print describe('Eddard Stark')
print describe('Cersei Lannister')
print relation_bw('Arya Stark', 'Myrcella Baratheon')
print relation_bw('Arya Stark', 'Lyanna Stark')
print relation_bw('Tommen Baratheon', 'Lyanna Stark')
print relation_of('Arya Stark', 'father')
print relation_of('Cersei Lannister', 'children')
print death('Joffrey Baratheon')
print death('Eddard Stark')

from pyquery import PyQuery
import re

def fetchInfoFromURL(URL):
    #URL = "http://gameofthrones.wikia.com/wiki/Gregor_Clegane"
    f = open('/home/abhinav/Eclipse/WebCrawler/CollectedInfo.txt', 'a')
    splitter=re.compile('/')
    tmp = splitter.split(URL)
    if (len(tmp) < 3):
        return 1
    splitter=re.compile('_')
    tmp = splitter.split(tmp[len(tmp)-1])
    character = ""
    for s in tmp:
        character = character + " " + s
    
    d = PyQuery(url=URL)
    TableLable =  d("#mw-content-text>aside h3.pi-data-label")
    TableValue = d("#mw-content-text>aside div.pi-data-value")
    
    #for i in range(0, len(TableLable)):
    #    print()
    
    #print(d("#mw-content-text>aside div.pi-data-value").text())
    
    print(len(TableLable), len(TableValue))
    if (len(TableLable) != len(TableValue) or len(TableLable) == 0):
        return 1
    
    f.write("{{{##" + character + "##}}}\n")
    for i in range(0,len(TableValue)):
        dd = PyQuery(TableValue.eq(i))
        stRow = "{{{" + TableLable.eq(i).text() + "}}} "
        stAttr = ""
        for j in range(0, len(dd.contents())):
            if (dd.contents()[j] != ' '):
                if (dd.contents().eq(j).text() != ""):
                    stAttr = stAttr + dd.contents().eq(j).text()
                else:
                    stRow = stRow + "{{{"+stAttr+"}}} "
                    stAttr=""
        if (stAttr !=""):
            stRow = stRow + "{{{"+stAttr+"}}} "
        f.write(stRow+"\n")
    f.write("\n\n")
    f.close()
    return 0


def main():
    f = open('/home/abhinav/Eclipse/WebCrawler/DataLinks.txt', 'r')
    i=0
    for line in f:
        i= i+1
        #if(i>0):
        #    break
        line = line[0:len(line)-1]
        #print("Processing "+line)
        if (fetchInfoFromURL(line)):
            print("Failed processing "+line)
        #else:
        #    print("Succeed")
    f.close()

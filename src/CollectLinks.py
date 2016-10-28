from html.parser import HTMLParser  
from urllib.request import urlopen  
from urllib import parse

# We are going to create a class called LinkParser that inherits some
# methods from HTMLParser which is why it is passed into the definition
class LinkParser(HTMLParser):

    # This is a function that HTMLParser normally has
    # but we are adding some functionality to it
    def handle_starttag(self, tag, attrs):
        # We are looking for the begining of a link. Links normally look
        # like <a href="www.someurl.com"></a>
        #print(tag)
        if tag=="a":
            for (key, value) in attrs:
                if key=="href":
                    # We are grabbing the new URL. We are also adding the
                    # base URL to it. For example:
                    # www.netinstructions.com is the base and
                    # somepage.html is the new URL (a relative URL)
                    #
                    # We combine a relative URL with the base URL to create
                    # an absolute URL like:
                    # www.netinstructions.com/somepage.html
                    #print(self.baseUrl, value)
                    
                    newUrl = parse.urljoin(self.baseUrl, value)
                    tmp = "http://gameofthrones.wikia.com/wiki/Category:Characters?page="
                    if  tmp in newUrl and "#" not in newUrl:
                    # And add it to our collection of links:
                        #print("Crawl URL" + newUrl)
                        self.linksToCrawl = self.linksToCrawl + [newUrl]
                    elif "http://gameofthrones.wikia.com/wiki/Category:" in newUrl:
                        #print("Discard URL" + newUrl)
                        continue
                    elif "http://gameofthrones.wikia.com/wiki/" in newUrl:
                        #print("Store URL" + newUrl)
                        self.linksToStore = self.linksToStore + [newUrl]

    # This is a new function that we are creating to get links
    # that our spider() function will call
    def getLinks(self, url):
        self.linksToCrawl = []
        self.linksToStore = []
        
        # Remember the base URL which will be important when creating
        # absolute URLs
        self.baseUrl = url
        #print(url)
        # Use the urlopen function from the standard Python 3 library
        response = urlopen(url)
        #response = response.read()
        #print(response)
        # Make sure that we are looking at HTML and not other things that
        # are floating around on the internet (such as
        #print(response.getheader('Content-Type'))
        
        # JavaScript files, CSS, or .PDFs for example)
        if 'text/html' in response.getheader('Content-Type'):
            htmlBytes = response.read()
            # Note that feed() handles Strings well, but not bytes
            # (A change from Python 2.x to Python 3.x)
            htmlString = htmlBytes.decode("utf-8")
            
            #print(htmlString)
            self.feed(htmlString)
            return htmlString, self.linksToCrawl, self.linksToStore
        else:
            return "",[]

# And finally here is our spider. It takes in an URL, a word to find,
# and the number of pages to search through before giving up
def spider(url, word, maxPages):  
    pagesToVisit = [url]
    pagesToStore = [url]
    pagesVisited = {}
    numberVisited = 0
    f = open('/home/abhinav/Eclipse/WebCrawler/DataLinks.txt', 'a')
    f.write("\n"+"\n")
    # The main loop. Create a LinkParser and get all the links on the page.
    # Also search the page for the word or string
    # In our getLinks function we return the web page
    # (this is useful for searching for the word)
    # and we return a set of links from that web page
    # (this is useful for where to go next)
    while numberVisited < maxPages and numberVisited < len(pagesToVisit):
        # Start from the beginning of our collection of pages to visit:
        url = pagesToVisit[numberVisited]
        numberVisited = numberVisited +1
        if url in pagesVisited:
            continue
        else:
            pagesVisited[url] = 1
        
        #pagesToVisit = pagesToVisit[1:]
        try:
            print(numberVisited, "Visiting:", url)
            parser = LinkParser()
            data, linksToCrawl, linksToStore = parser.getLinks(url)
                # Add the pages that we visited to the end of our collection
                # of pages to visit:
            print(len(linksToCrawl))
            print(len(linksToStore))
            pagesToVisit = pagesToVisit + linksToCrawl
            pagesToStore = pagesToStore + linksToStore
            pagesToStore = list(set(pagesToStore))
        except:
            print(" **Failed!**")
    #print(pagesToStore)
    print(len(pagesToStore))
    print(len(pagesVisited))
    for s in pagesToStore:
        f.write(s+"\n")
    f.close()
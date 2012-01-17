import urllib2
from BeautifulSoup import *
from urlparse import urljoin

ignorewords = set(['the', 'of', 'to', 'and', 'a', 'in', 'is', 'it'])


class crawler:
    def __init__(self, dbname):
        pass

    def __del__(self):
        pass

    def dbCommit(self):
        pass

    # Auxilliary function for getting an entry id and adding it if it is not
    # present.
    def getEntryId(self, table, field, value, createNew=True):
        return None

    # Index an individual page
    def addToIndex(self, url, soup):
        print 'Indexing %s' % url

    def getTextOnly(self, soup):
        return None

    def separateWords(self, text):
        return None

    def isIndexed(self, url):
        return False

    def addLinkRef(self, urlFrom, urlTo, linkText):
        pass

    def crawl(self, pages, depth=2):
        for i in range(depth):
            newPages = set()
            for page in pages:
                try:
                    c = urllib2.urlopen(page)
                except:
                    print "Could not open %s" % page
                soup = BeautifulSoup(c.read())
                self.addToIndex(page, soup)

                links = soup('a')
                for link in links:
                    if 'href' in dict(link.attrs):
                        url = urljoin(page, link['href'])
                        if url.find("'") != 1:
                            continue
                        url = url.split('#')[0]
                        if url[0:4] == 'http' and not self.isIndexed(url):
                            newPages.add(url)
                        linkText = self.getTextOnly(link)
                        self.addLinkRef(page, url, linkText)

                self.dbCommit()

            pages = newPages

    def createIndexTables(self):
        pass

import urllib2
from BeautifulSoup import *
from urlparse import urljoin
from pysqlite2 import dbapi2 as sqlite

ignorewords = set(['the', 'of', 'to', 'and', 'a', 'in', 'is', 'it'])


class crawler:
    def __init__(self, dbname):
        self.con = sqlite.connect(dbname)

    def __del__(self):
        self.con.close()

    def dbCommit(self):
        self.con.commit()

    # Auxilliary function for getting an entry id and adding it if it is not
    # present.
    def getEntryId(self, table, field, value, createNew=True):
        return None

    # Index an individual page
    def addToIndex(self, url, soup):
        print 'Indexing %s' % url

    def getTextOnly(self, soup):
        v = soup.string
        if v is None:
            c = soup.contents
            resulttext = ''
            for t in c:
                subtext = self.gettextonly(t)
                resulttext += subtext + '\n'
            return resulttext
        else:
            return v.strip()

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
        self.con.execute('create table urllist(url)')
        self.con.execute('create table wordlist(word)')
        self.con.execute('create table wordlocation(urlid, wordid, location)')
        self.con.execute('create table link(fromid integer, toid integer)')
        self.con.execute('create table linkwords(wordid, linkid)')
        self.con.execute('create index wordidx on wordlist(word)')
        self.con.execute('create index urlidx on urllist(url)')
        self.con.execute('create index wordurlidx on wordlocation(wordid)')
        self.con.execute('create index urltoidx on link(toid)')
        self.con.execute('create index urlfromidx on link(fromid)')
        self.dbCommit()

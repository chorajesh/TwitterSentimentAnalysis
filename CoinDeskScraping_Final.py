# this program scrapes CoinDesk and gets metadata about cryptocurrency articles
# that metadata will be used for analysis and to get the full article text using
# another script, get

from urllib.request import urlopen
import urllib.parse
from bs4 import BeautifulSoup
import re


# https://www.coindesk.com/?s=bitcoin

def getArticleContent(aricleLink):
    articleContentPageSoup = getsource(aricleLink)[0]
    articleContent = ""
    for paras in articleContentPageSoup.find('div', {'class': 'article-content-container noskimwords'}).findAll('p'):
        articleContent += paras.getText()
    return articleContent


def getsource(url):
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'})  # sends GET request to URL
    uClient = urllib.request.urlopen(req)
    # html = urlopen(url)
    # pageHtml = html.read()
    # bsObj = BeautifulSoup(pageHtml, "lxml")
    pageHtml = uClient.read()  # reads returned data and puts it in a variable
    uClient.close()  # close the connection
    pageSoup = BeautifulSoup(pageHtml, 'lxml')
    return [pageSoup, pageHtml]


def getArticleInfo(coinDeskScrapeSoup):
    articleDetails = []
    for content in coinDeskScrapeSoup.findAll('div', {'id': 'content'}):
        # print(content)
        for postDiv in content.findAll('div', {'class': 'post-info'}):
            href = postDiv.a.get('href')
            articleContent = getArticleContent(href)
            title = postDiv.a.get('title')
            time = postDiv.find('p', {'class': 'timeauthor'}).time.getText()
            desc = postDiv.find('p', {'class': 'desc'}).getText()
            cite = postDiv.find('p', {'class': 'timeauthor'}).cite.getText().strip()
            myList = [href, title, time, desc, cite]
            articleDetails = articleDetails + myList
    return articleDetails


# lets find the first page and the last page, lets write a function
# need to get the page numbers (last page has >> )

def getLastPageNumber(coinDeskScrapeSoup):
    for page in coinDeskScrapeSoup.findAll('div', {'class': 'pagination'}):
        # print(page)
        for anchors in page.findAll('a'):
            if (anchors.getText() == '»'):
                lastPage = anchors.get('href')
                startIndex = lastPage.index('page/') + 5
                endIndex = lastPage.index('/?')
                lastPageNumber = lastPage[startIndex:endIndex]

    return lastPageNumber


baseURL = r'https://www.coindesk.com/'
searchQuery = '?s='
term = "bitcoin"

url = baseURL + searchQuery + urllib.parse.quote_plus(term)
# print(url)
sourceDetails = getsource(url)  # gets the whole source code
pageHtmlCode = sourceDetails[1]
coinDeskScrapeSoup = sourceDetails[0]
# print(coinDeskScrapeSoup)

firstPage = 1
lastPage = int(getLastPageNumber(coinDeskScrapeSoup))

for pageNumber in range(firstPage, lastPage + 1):
    articlePageUrl = baseURL + 'page/' + str(pageNumber) + '/' + searchQuery + urllib.parse.quote_plus(term)
    eachPageSoup = getsource(articlePageUrl)[0]
    eachPageArticleInfo = getArticleInfo(eachPageSoup)
    print(eachPageArticleInfo)

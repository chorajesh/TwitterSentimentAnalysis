# this program scrapes CoinDesk and gets metadata about cryptocurrency articles
# that metadata will be used for analysis and to get the full article text using
# another script, getEachContent_Final.py

from urllib.request import urlopen
import urllib.parse
from bs4 import BeautifulSoup
import re
import pandas as pd, numpy as np

#https://www.coindesk.com/?s=bitcoin

#Get the article content of the link provided.

def getArticleContent(aricleLink):
    articleContentPageSoup = getsource(aricleLink)[0]
    articleContent = ""
    for paras in articleContentPageSoup.find('div', {'class':'article-content-container noskimwords'}).findAll('p'):
        articleContent += paras.getText()
    return articleContent
        
#get the beautiful soup object for the url specified.
def getsource(url):
    req=urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}) #sends GET request to URL
    uClient=urllib.request.urlopen(req)
    #html = urlopen(url)
    #pageHtml = html.read()
    #bsObj = BeautifulSoup(pageHtml, "lxml")
    pageHtml=uClient.read() #reads returned data and puts it in a variable
    uClient.close() #close the connection
    pageSoup=BeautifulSoup(pageHtml,'lxml')
    return [pageSoup, pageHtml]

# get the meta data of the article such as Article title, link, author, published time and short descripion
def getArticleInfo(coinDeskScrapeSoup):
    articleDetails = []
    for content in coinDeskScrapeSoup.findAll('div', {'id':'content'}):
       # print(content)
        for postDiv in content.findAll('div', {'class':'post-info'}):
            try:
                href = postDiv.a.get('href') 
                #articleContent = getArticleContent(href)
                title = postDiv.a.get('title')
                time = postDiv.find('p', {'class':'timeauthor'}).time.getText()
                desc = postDiv.find('p', {'class':'desc'}).getText()
                cite = postDiv.find('p', {'class':'timeauthor'}).cite.getText().strip()
                mydf = pd.DataFrame({'link': href,
                                     'title': title,
                                     'published': time,
                                     'desc': desc,
                                     'author': cite}, index = [0])
                articleDetails.append(mydf)
            except:
               mydf = pd.DataFrame({'link': 'exception error',
                                    'title': 'exception error',
                                    'published': 'exception error',
                                    'desc': 'exception error',
                                    'author': 'exception error'}, index = [0])
               articleDetails.append(mydf)
               pass

    articleDetails = pd.concat(articleDetails)
    return articleDetails
#lets find the first page and the last page, lets write a function 
#need to get the page numbers (last page has >> )

def getLastPageNumber(coinDeskScrapeSoup):
    for page in coinDeskScrapeSoup.findAll('div', {'class':'pagination'}):
    #print(page)
        for anchors in page.findAll('a'):
            if (anchors.getText()=='»'):
                lastPage = anchors.get('href')
                startIndex = lastPage.index('page/') + 5
                endIndex = lastPage.index('/?')
                lastPageNumber = lastPage[startIndex:endIndex]
                
    return lastPageNumber


        

baseURL = r'https://www.coindesk.com/'
searchQuery = '?s='
term = "litecoin"

url = baseURL + searchQuery + urllib.parse.quote_plus(term)
#print(url)
sourceDetails = getsource(url) #gets the whole source code
pageHtmlCode = sourceDetails[1]
coinDeskScrapeSoup = sourceDetails[0]
#print(coinDeskScrapeSoup)

firstPage = 1
lastPage = int(getLastPageNumber(coinDeskScrapeSoup))
#lastPage = 5

article_list = []
for pageNumber in range(firstPage,lastPage + 1):
    articlePageUrl = baseURL + 'page/' + str(pageNumber) + '/' + searchQuery + urllib.parse.quote_plus(term)
    eachPageSoup = getsource(articlePageUrl)[0]
    eachPageArticleInfo = getArticleInfo(eachPageSoup)
    article_list.append(eachPageArticleInfo)
    print(str(pageNumber) + ' / ' + str(lastPage))

article_df = pd.concat(article_list)


    
article_df_copy = article_df

article_df_copy['title'] = article_df_copy['title'].str.replace(',', '')
article_df_copy['published'] = article_df_copy['published'].str.replace(',', '')
article_df_copy['desc'] = article_df_copy['desc'].str.replace(',', '')
article_df_copy['author'] = article_df_copy['author'].str.replace(',', '')

article_df_copy.to_csv('./article_df.csv')






    


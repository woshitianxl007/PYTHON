#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import urllib2
import re
from bs4 import BeautifulSoup

def getHtml(url):
    page = urllib2.urlopen(url)
    html = page.read()
    return html

def prints(html):
    soup = BeautifulSoup(html,"html.parser")
    soup.prettify()
    #soup = soup.findAll('ol', class_= 'grid_view')
    soup = soup.findAll('div', class_= 'pic')
    f = open('doubantop250.txt', 'a')
    for s in soup:
        #print s.get_text()
        a = "INSERT INTO DOUBAN_MOVIES VALUES(ID,MOVIE_NAME,MOVIES_HREF), (" + s.find('em').get_text()+ ", '" + s.find('img')['alt']+"', '"+ s.find('a')['href']+"')"
        print s.find('em').get_text()+ '_' + s.find('img')['alt']+'_'+'"'+ s.find('a')['href']+'"'
        f.write(a)
        f.write("\n")
    f.close()
if __name__=='__main__':
    f = open('doubantop250.txt', 'w')
    f.write("CREATE TABLE DOUBAN_MOVIES()")
    f.close()
    num = 0
    for s in range(0,10):
        num =s*25
        url = 'http://movie.douban.com/top250?start=' + str(num) + '&filter='
        html = getHtml(url)
        prints(html)


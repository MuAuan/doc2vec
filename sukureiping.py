#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv

try:
    # Python 3
    from urllib import request
except ImportError:
    # Python 2
    import urllib2 as request

from bs4 import BeautifulSoup

def getNavigableStrings(soup):
  if isinstance(soup, BeautifulSoup.NavigableString):
    if type(soup) not in (BeautifulSoup.Comment,
      BeautifulSoup.Declaration) and soup.strip():
      yield soup
  elif soup.name not in ('script', 'style'):
    for c in soup.contents:
      for g in getNavigableStrings(c):
        yield g

def main():
    # 永久に実行させます
    # ブログから Content-Body を取得する
    for i in range(1,31,1):
        response = request.urlopen('http://www.jma.go.jp/jma/kishou/know/faq/faq' + str(i) +'.html')
        body = response.read()
        # HTML をパースする
        soup = BeautifulSoup(body,"html.parser")
    
        for td in soup("div", {"id":"main"}):
            if td =="":
                pass
            else:
                ts=td
                print(ts)
    
        csv_list_t = []
        ft = open('T.html', 'a')
    
        for s in ts(['script','style']):
            s.decompose()
    
        #text = '\t\n'.join(ts.stripped_strings)
        text = ts

        
        writert = csv.writer(ft, lineterminator='\n')
        csv_list_t.append(text)
        writert.writerow(csv_list_t)

        ft.close()
if __name__ == '__main__':
    main()


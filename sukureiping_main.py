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


def main():
    # 永久に実行させます
    # ブログから Content-Body を取得する
    response = request.urlopen('http://www.jma.go.jp/jma/kishou/know/faq/faq18.html')
    body = response.read()
    #print(body)
    # HTML をパースする
    soup = BeautifulSoup(body,"html.parser")
        # csvに記述するレコードを作成します
    csv_list_q = []
    csv_list_a = []
    print(soup)



    #while True:
        # csvを追記モードで開きます→ここでcsvを開くのはファイルが大きくなった時にcsvを開くのに時間がかかるためです
    fq = open('Q.csv', 'a')
    fa = open('A.csv', 'a')
    writerq = csv.writer(fq, lineterminator='')
    writera = csv.writer(fa, lineterminator='')

    # print時のエラーとならないように最初に宣言しておきます。
    question = []
    answer = []
    
    # class 属性が mtx である tr タグを対象に

    for td in soup("div", {"id":"main"}):
        # 各データを取得
        for tr in td("h2"):
            if tr.string == "":
                pass
            else:
                question = tr.string +"\n"
            print(question)
            csv_list_q.append(question)
        for ts in td("p", {"class":"mtx"}):
            if ts.string == "":
                pass
            else:
                answer = ts.string
            print(answer)
            csv_list_a.append(answer)
    #for i in range (len(question)):
        #csv_list.append(question)
     #   csv_list.append(question+answer)
        #csv_list.append(answer)
        
    writerq.writerow(csv_list_q)
    writera.writerow(csv_list_a)
    # ファイル破損防止のために閉じます
    fq.close()
    fa.close()
if __name__ == '__main__':
    main()


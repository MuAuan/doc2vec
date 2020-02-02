#!/usr/bin/env python                               
# -*- coding: utf-8 -*-


from twitter import *
#import api
from twython import Twython 
#from api import PostUpdate
import MeCab
import zenhan
from requests_oauthlib import OAuth1Session
import json
import argparse
import re
import datetime # datetimeモジュールのインポート
import locale   # import文はどこに書いてもOK(可読性などの為、慣例でコードの始めの方)

### Constants                                                                                                                                                     
oath_key_dict = {
    "consumer_key": "************************",
    "consumer_secret": "************************************************",
    "access_token": "************************************************",
    "access_token_secret": "************************************************"
}

### Functions                                                                                                   
parser = argparse.ArgumentParser()
parser.add_argument("--dictionary", "-d", type=str, help="mecab dictionary")
args = parser.parse_args()


mecab = MeCab.Tagger("" if not args.dictionary else " -d " + args.dictionary)
#"助詞","助動詞","副詞","記号","動詞","名詞"
def wakati(str):
    words = []
    for line in mecab.parse(zenhan.z2h(str, mode=3).lower()).split("\n"):
        cols = line.split("\n")
        if len(cols) >= 2:
            c = cols[1].split(",")
            if not c[0] in ["助詞","助動詞","副詞","記号","動詞","名詞"] and not c[1] in ["非自立","代名詞"]:
                words.append(cols[0])
    return words

def wakeru(str):
    #words = []
    words = re.sub(r'[^一-龥ぁ-んァ-ン]', "", str)
    return words

def wakeru2(str):
    #words = []
    words = re.sub(r'[一-龥ぁ-んァ-ン]', "", str)
    return words

def main():
    consumer_key= "************************"
    consumer_secret= "************************************************"
    access_token= "************************************************"
    access_token_secret= "************************************************"
    auth=OAuth(access_token, access_token_secret, consumer_key, consumer_secret)
    # タイムライン取得用のURL
    url = "https://api.twitter.com/1.1/statuses/home_timeline.json"
    url1 = "https://api.twitter.com/1.1/search/tweets.json"

    # とくにパラメータは無い
    keyword = "#question"
    params = {'q' : '#回答', 'count' : 100, 'result_type' : 'recent'}
    #params = {}
    #t = Twitter(auth=auth)
    #t = OAuth1Session(consumer_key, consumer_secret, access_token, access_token_secret)
    d = datetime.datetime.today()
    ds = d + datetime.timedelta(minutes=1)
    print( ds.strftime("%x,%X"),d.strftime("%x,%X"))
    tw_old=[]
    x=[]
    y=[]
    while True:
        if d > ds:
            t = OAuth1Session(consumer_key, consumer_secret, access_token, access_token_secret)
            print( ds.strftime("%x,%X"),d.strftime("%x,%X"))
            ds = d + datetime.timedelta(minutes=10)
        
            # Search for the latest tweets about #pycon
            req = t.get(url1, params = params)

            if req.status_code == 200:
            # レスポンスはJSON形式なので parse する
                timeline = json.loads(req.text)
                
            # 各ツイートの本文を表示
                f = open("test_arukai.txt", "w", encoding="utf-8")
                
                for tweet in timeline['statuses']:
                    x = tweet['text']
                    print(x)
                    y = tweet['user']['screen_name']
                    print(y)
                    tw=x
                    if tw!=tw_old:
                        print(tw)
                        ts=wakeru(tw)
                        print(ts)
                        f.write(str(ts)+" "+str(y)+"\n")
                        tw_old=tw
                        
                    else:
                        continue
                f.close()
            
            else:
            # エラーの場合
                print ("Error: %d" % req.status_code)
        else:
            d=datetime.datetime.today()
        
    return

def tweet(desc,t):
    content = '@muauan_bot'
    for item in desc:
        #content += ' ' 
        content += item
    content += '#TweetByBot'
    # Update your status
    
    print(content) 
    t.statuses.update(status=content)
    return

def create_oath_session(oath_key_dict):
    oath = OAuth1Session(
    oath_key_dict["consumer_key"],
    oath_key_dict["consumer_secret"],
    oath_key_dict["access_token"],
    oath_key_dict["access_token_secret"]
    )
    return oath
        

def tweet_search(search_word, oath_key_dict):
    url = "https://api.twitter.com/1.1/search/tweets.json?"
    keyword = u''+str(search_word)+' URIエンコード'
    params = {
        "q": keyword.encode("utf-8"),
        "lang": "ja",
        "result_type": "recent",
        "count": "15"
        }
    oath = create_oath_session(oath_key_dict)
    responce = oath.get(url, params = params)
    if responce.status_code != 200:
        print( "Error code: %d" %(responce.status_code))
        return None
    tweets = json.loads(responce.text)
    return tweets

### Execute                                                                                                                                                       
if __name__ == "__main__":
    #tweet("test2")
    main()

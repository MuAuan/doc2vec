#$ python3 tweet_bot_get.py
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
    words = re.sub(r'[質問]', "", words)
    return words

def wakeru2(str):
    #words = []
    words = re.sub(r'[^#muauan_bot]', "", str)
    return words

def tweet_get(t,params,tw_old,url1):
                # Search for the latest tweets about #pycon
    req = t.get(url1, params = params)
    print("req.status_code=",req.status_code)
    x=[]
    if req.status_code == 200:
            # レスポンスはJSON形式なので parse する
        timeline = json.loads(req.text)
        #print(timeline)        
            # 各ツイートの本文を表示
        for tweet in timeline: #['statuses']:
            print(tweet['text'])
            wt=wakeru2(tweet['text'])
            print(wt)
            if wt=='#muauan_bot':
                x = tweet['text']
                print(x)
                #tw=x
                y = tweet['user']['screen_name']
                #print(y)
                break
            else:
                continue

    else:
            # エラーの場合
        print ("Error: %d" % req.status_code)
        return
    
    tw=x
    if tw!=tw_old:
        print(tw,y)
        ts=wakeru(tw)
        #print(ts)
        f = open("test1.txt", "w", encoding="utf-8")
        f.write(str(ts)+" @"+str(y))
        tw_old=tw
        f.close()
    #else:
     #   continue
    return tw
    
def main():
    consumer_key= "************************"
    consumer_secret= "************************************************"
    access_token= "************************************************"
    access_token_secret= "************************************************"
    auth=OAuth(access_token, access_token_secret, consumer_key, consumer_secret)
    t1 = Twitter(auth=auth)

    # タイムライン取得用のURLと検索用URL1
    url = "https://api.twitter.com/1.1/statuses/home_timeline.json"
    url1 = "https://api.twitter.com/1.1/search/tweets.json"

    # とくにパラメータは無い
    keyword = "#question"
    #params = {'q' : '#muauan_bot', 'count' : 1, 'result_type' : 'recent'} #,'since_id':944871419761999873}
    params = {'count' : 20} #,'since_id':944871419761999873}
    sentences_old=[]

    #t = Twitter(auth=auth)
    #t = OAuth1Session(consumer_key, consumer_secret, access_token, access_token_secret)
    d = datetime.datetime.today()
    ds = d + datetime.timedelta(minutes=1)
    print( ds.strftime("%x,%X"),d.strftime("%x,%X"))
    tw_old=[]
    tex_old=[]
    n =0
    while True:
        ss=True
        while ss:
            while d < ds:
                d=datetime.datetime.today()
            else:
                t = OAuth1Session(consumer_key, consumer_secret, access_token, access_token_secret)
                print( ds.strftime("%x,%X"),d.strftime("%x,%X"))
                ds = d + datetime.timedelta(minutes=3)
                tex=tweet_get(t,params,tw_old,url)
                if tex != tex_old:
                    tex_old =tex
                    ss =False
                    break
            print(tex)
            text = open("test2.txt",'r',encoding='utf8', errors='ignore', buffering=1).read().lower()
            sentences = text[0:125] #+wakeru2(text)
            if sentences not in [sentences_old, ""]:
                # Update your status
                sentence=tweet(sentences,t1,n)
                sentences_old = sentences
                break
            else:
                continue
        f = open("test2.txt", "w", encoding="utf-8")
        f.write(str(""))
        n += 1
    else:
        return
    return

def tweet(desc,t,n):
    content = '#回答 '
    """
    for item in desc:
        item = wakeru(item)
        #content += ' ' 
        content += item
    content = content+wakeru2(desc)+" "+str(n)
    """
    content += desc +" "+str(n) 
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
        

### Execute                                                                                                                                                       
if __name__ == "__main__":
    #tweet("test2")
    main()

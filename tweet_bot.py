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
    "consumer_key": "****************J",
    "consumer_secret": "***********************************",
    "access_token": "************************************",
    "access_token_secret": "*************************************"
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
    words = re.sub(r'[ダミー]', "", words)
    return words

def wakeru2(str):
    #words = []
    words = re.sub(r'[一-龥ぁ-んァ-ン]', "", str)
    return words

def main():
    consumer_key= "************************"
    consumer_secret= "************************************"
    access_token= "*************************************"
    access_token_secret= "******************************************"
    auth=OAuth(access_token, access_token_secret, consumer_key, consumer_secret)
    t = Twitter(auth=auth)

    #Get your "home" timeline
    #print(t.statuses.home_timeline(count=5))
    """
    # Send a direct message
    t.direct_messages.new(
    user="muauan",
    text="I think yer swell!")
     
    
    print(sentence) 
    t.statuses.update(status=sentence)
    """
    #tweets = tweet_search("事例", oath_key_dict)
    #print(tweets)
    d = datetime.datetime.today()
    sentences_old=[]
    ds=d + datetime.timedelta(minutes=3) #3分減算
    print( ds.strftime("%x,%X"),d.strftime("%x,%X"))
    n =0
    while True:
        if d > ds:
            print( ds.strftime("%x,%X"),d.strftime("%x,%X"))
            ds = d + datetime.timedelta(minutes=3)
            text = open("test2.txt",'r',encoding='utf8', errors='ignore', buffering=1).read().lower()
            print(text)

            sentences = text[0:120] +wakeru2(text)
            if sentences not in [sentences_old,""]:
                # Update your status
                sentence=tweet(sentences,t,n)
                sentences_old = sentences
            else:
                continue
        
            f = open("test2.txt", "w", encoding="utf-8")
            f.write(str(""))
            #tweet("test2")
            n += 1
        else:
            d=datetime.datetime.today()
    return

def tweet(desc,t,n):
    content = '#回答 '
    
    for item in desc:
        item = wakeru(item)
        #content += ' ' 
        content += item
    content += ' '+ wakeru2(desc)
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

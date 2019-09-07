# -*- coding: utf-8 -*-
"""
$python3 tfidf_fasttext.py JMA_FAQ.lst wiki_all_model300 -d /usr/lib/mecab/dic/mecab-ipadic-neologd
$python3 tfidf_fasttext.py JMA_FAQ.lst wiki_all_model300.bin -d /usr/share/mecab/dic/mecab-ipadic-neologd
"""

#from gensim.models.wrappers.fasttext import FastText
#from gensim.models.fasttext import FastText
from gensim.models import FastText
import MeCab
import zenhan
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import argparse

DIM = 300

parser = argparse.ArgumentParser()
parser.add_argument('input', type=str)
parser.add_argument('model', type=str)
parser.add_argument("--dictionary", "-d", type=str, help="mecab dictionary")
args = parser.parse_args()

mecab = MeCab.Tagger("" if not args.dictionary else " -d " + args.dictionary)

def wakati(str):
    words = []
    for line in mecab.parse(zenhan.z2h(str, mode=3).lower()).split("\n"):
        cols = line.split("\t")
        if len(cols) >= 2:
            c = cols[1].split(",")
            if not c[0] in ["助詞","助動詞","副詞","記号"] and not c[1] in ["非自立","代名詞"]:
                words.append(cols[0])
    return words


questions_src = []
questions = []
answers = []
for line in open(args.input, "r", encoding="utf-8",errors="ignore"):
    cols = line.strip().split('\t')
    #print(cols[0])
    questions_src.append(cols[0])
    questions.append(wakati(cols[0]))
    answers.append(cols[1])

model = FastText.load_fasttext_format(args.model)

def part_minus(v):
    #正と負で別のベクトルにする
    tmp_v = np.zeros(DIM*2)
    for i in range(DIM):
        if v[i] >=0:
            tmp_v[i] = v[i]
        else:
            tmp_v[i*2] = - v[i]
    return tmp_v

        

questions_vec = []
tf_vecs = []
df_vec = np.zeros(DIM*2)
for question in questions:
    vec = np.zeros(DIM*2)
    maxvec = np.zeros(DIM*2)
    for word in question:
        try:
            word_vec = part_minus(model[word])
            vec += word_vec
        except:
            continue
        maxvec = np.maximum(word_vec, maxvec)
    #print(vec, sum(vec))
    tf_vecs.append(vec/sum(vec))
    df_vec += maxvec
    
idf_vec = np.log(len(questions)/(df_vec + 1))
tfidf_vecs = []
for tf_vec in tf_vecs:
    tfidf_vecs.append(tf_vec*idf_vec)
    
while True:
    line = input(">")
    if not line:
        break
        
    words = wakati(line)
    vec = np.zeros(DIM*2)
    for word in words:
        try:
            vec += part_minus(model[word])
        except:
            continue
    tf_vec = vec/sum(vec)
    
    sims = cosine_similarity([tf_vec*idf_vec], tfidf_vecs)
    index = np.argsort(sims[0])
       
    print(" ",words)
    print(questions_src[index[-1]], sims[0,index[-1]])
    print()
    print(answers[index[-1]])
    print()
    print(questions_src[index[-2]], sims[0,index[-2]])
    print(questions_src[index[-3]], sims[0,index[-3]])
    print(questions_src[index[-4]], sims[0,index[-4]])
    print(questions_src[index[-5]], sims[0,index[-5]])
    print()

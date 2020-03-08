#$ python3 anzen_qtrain_doc2vec.py conversation_anzen.csv -d /usr/lib/aarch64-linux-gnu/mecab/dic/mecab-ipadic-neologd -s stop_words.txt

import gensim
from gensim import models
import MeCab
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import argparse
import smart_open
import re

parser = argparse.ArgumentParser()
parser.add_argument('faq', type=str)
#parser.add_argument('model', type=str)
parser.add_argument("--dictionary", "-d", type=str, help="mecab dictionary")
parser.add_argument("--stop_words", "-s", type=str, help="stop words list")
args = parser.parse_args()

mecab = MeCab.Tagger("-Owakati" + ("" if not args.dictionary else " -d " + args.dictionary))

questions = []
sentences = []
originals=[]
j = 0
for line in open(args.faq, "r", encoding="cp932"): #utf-8
    cols = line.strip().split('\n')  #t
    questions.append(gensim.utils.simple_preprocess(mecab.parse(cols[0]).strip(), min_len=1)) #1
    originals.append(cols[0]) 
    sentences.append(models.doc2vec.TaggedDocument(gensim.utils.simple_preprocess(mecab.parse(cols[0]).strip(), min_len=1), tags=["SENT_"+str(j)]))
    j += 1

stop_words = []
if args.stop_words:
    for line in open(args.stop_words, "r", encoding="utf-8"):
        stop_words.append(line.strip())

vectorizer = TfidfVectorizer(token_pattern="(?u)\\b\\w+\\b", stop_words=stop_words)

model = models.Doc2Vec(vector_size=400, windows=5, min_count=5, epochs=100)

model.build_vocab(sentences)
"""
print('\n訓練開始')
for epoch in range(51):
    print('Epoch: {}'.format(epoch + 1))
    model.train(sentences, epochs=model.epochs, total_examples=model.corpus_count)
    if epoch%5==0:
        model_str="jamQ_model400_doc2vec_"+str(epoch)
        model.save(model_str)
"""
model_str="jamQ_model400_doc2vec_50"
model = models.Doc2Vec.load(model_str) 

doc_vecs = []
for question in questions:
    doc_vecs.append(model.infer_vector(question))
    
while True:
    line = input("> ")
    if not line:
        break

    vec = model.infer_vector(gensim.utils.simple_preprocess(mecab.parse(line), min_len=1))
    sims = cosine_similarity([vec], doc_vecs)
    index = np.argsort(sims[0])

    #print(originals[index[-1]])
    print()
    sk=0
    targets = []
    targets_ = []
    for j in range(-1,-100,-1):
        if sims[0][index[j]]>=0.2:
            print("{}_({:.2f}): {}".format(sk,sims[0][index[j]],originals[index[j]]))
            targets.append(mecab.parse(originals[index[j]]).strip())
            targets_.append("{}d2v({:.2f}):{}".format(sk,sims[0][index[j]],originals[index[j]]))
            sk += 1    
    print("______________tf-idf____________")        
    vecs = vectorizer.fit_transform(targets)
    sims2 = cosine_similarity(vectorizer.transform([mecab.parse(line)]), vecs)    
    index2 = np.argsort(sims2[0])
    sk2=0
    for j in range(-1,-100,-1):
        if sims[0][index[j]]>=0.2:
            print("{}_tfidf({:.2f}): {}".format(sk2,sims2[0][index2[j]],targets_[index2[j]]))
            #print()
            sk2 += 1
    

            
#>python anzen_qtrain_doc2vec.py conversation_sisho.txt -d C:\PROGRA~1\mecab\dic\ipadic

import gensim
from gensim import models
import MeCab
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import argparse
import smart_open
import re

parser = argparse.ArgumentParser()
parser.add_argument('faq', type=str)
#parser.add_argument('model', type=str)
parser.add_argument("--dictionary", "-d", type=str, help="mecab dictionary")
args = parser.parse_args()

mecab = MeCab.Tagger("-Owakati" + ("" if not args.dictionary else " -d " + args.dictionary))

questions = []
sentences = []
j = 0
for line in open(args.faq, "r"):  #, encoding="utf-8"): #utf-8
    cols = line.strip().split('\n')  #t
    questions.append(gensim.utils.simple_preprocess(mecab.parse(cols[0]).strip(), min_len=1)) #1
    sentences.append(models.doc2vec.TaggedDocument(gensim.utils.simple_preprocess(mecab.parse(cols[0]).strip(), min_len=1), tags=["SENT_"+str(j)]))
    j += 1

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

    #print(questions[index[-1]])
    print()
    for i in range(1,5):
        line=questions[index[-i]]
        #print(line)
        line_=""
        for i in range(len(line)):
            #print(line[i])
            line_ += line[i]
        print(line_)
    
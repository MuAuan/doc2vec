#$ python3 jam_qa_doc2vec.py JMA_FAQ.lst wiki10_model200_doc2vec_50 -d /usr/share/mecab/dic/mecab-ipadic-neologd
#$ python3 jam_qa_qtrain_doc2vec.py JMA_FAQ.lst -d /usr/share/mecab/dic/mecab-ipadic-neologd

import gensim
from gensim import models
import MeCab
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import argparse
import smart_open

parser = argparse.ArgumentParser()
parser.add_argument('faq', type=str)
#parser.add_argument('model', type=str)
parser.add_argument("--dictionary", "-d", type=str, help="mecab dictionary")
args = parser.parse_args()
"""
def read_corpus(fname):
    #with smart_open.smart_open(fname, encoding="utf-8") as f:
    with smart_open.open(fname, encoding="utf-8") as f:    
        for i, line in enumerate(f):
            # For training data, add tags
            yield models.doc2vec.TaggedDocument(gensim.utils.simple_preprocess(line, min_len=1), tags=["SENT_"+str(i)])
"""
mecab = MeCab.Tagger("-Owakati" + ("" if not args.dictionary else " -d " + args.dictionary))

#model = gensim.models.Doc2Vec.load(args.model)

questions = []
sentences = []
answers = []
j = 0
for line in open(args.faq, "r", encoding="utf-8"):
    cols = line.strip().split('\t')
    questions.append(gensim.utils.simple_preprocess(mecab.parse(cols[0]).strip(), min_len=1)) #1
    sentences.append(models.doc2vec.TaggedDocument(gensim.utils.simple_preprocess(mecab.parse(cols[0]).strip(), min_len=1), tags=["SENT_"+str(j)]))
    sentences.append(models.doc2vec.TaggedDocument(gensim.utils.simple_preprocess(mecab.parse(cols[1]).strip(), min_len=1), tags=["SENT_"+str(j+1)]))
    answers.append(cols[1])
    j += 2

model = models.Doc2Vec(vector_size=400, windows=5, min_count=5, epochs=100)

model.build_vocab(sentences)

print('\n訓練開始')
for epoch in range(51):
    print('Epoch: {}'.format(epoch + 1))
    model.train(sentences, epochs=model.epochs, total_examples=model.corpus_count)
    #model.alpha = 0.025 #(0.05 - 0.001) / 49
    #model.min_alpha = model.alpha
    if epoch%5==0:
        model_str="jamQ_model400_doc2vec_"+str(epoch)
        model.save(model_str)
    
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

    print(questions[index[-1]])
    print()
    print(answers[index[-1]])
    print()
    for i in range(2,5):
        print(questions[index[-i]])

    print()
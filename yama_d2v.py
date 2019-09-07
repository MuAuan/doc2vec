import gensim
import MeCab
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('faq', type=str)
#parser.add_argument('a', type=str)
#parser.add_argument('model', type=str)
parser.add_argument("--dictionary", "-d", type=str, help="mecab dictionary")
args = parser.parse_args()

mecab = MeCab.Tagger("-Owakati" + ("" if not args.dictionary else " -d " + args.dictionary))

#model = gensim.models.Doc2Vec.load(args.model)
model = gensim.models.Doc2Vec.load("my_model.doc2vec")   #model_doc2vec")

questions = []
answers = []
for line in open(args.faq, "r", encoding="utf-8"):
    cols = line.strip().split('\t')
    #print(cols[0])
    questions.append(gensim.utils.simple_preprocess(mecab.parse(cols[0]).strip(), min_len=1))
    answers.append(cols[1])
    
"""
for line in open(args.a, "r", encoding="utf-8"):
    cols = line.strip().split('\t')
    print(cols[0])
    answers.append(cols[0])
"""
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

    print(questions[index[-2]])
    print(questions[index[-3]])
    print(questions[index[-4]])
    print()
    print(questions[index[-5]])
    print(questions[index[-6]])
    print(questions[index[-7]])
    print()

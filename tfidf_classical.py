#$ python3 tfidf_classical.py JMA_FAQ.lst -d /usr/share/mecab/dic/mecab-ipadic-neologd -s stop_words.txt


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import MeCab

import argparse

parser = argparse.ArgumentParser(description="convert csv")
parser.add_argument("input", type=str, help="faq tsv file")
parser.add_argument("--dictionary", "-d", type=str, help="mecab dictionary")
parser.add_argument("--stop_words", "-s", type=str, help="stop words list")
args = parser.parse_args()

mecab = MeCab.Tagger("-Owakati" + ("" if not args.dictionary else " -d " + args.dictionary))

questions = []
answers = []
for line in open(args.input, "r", encoding="utf-8"):
    cols = line.strip().split('\t')
    questions.append(mecab.parse(cols[0]).strip())
    answers.append(cols[1])

stop_words = []
if args.stop_words:
    for line in open(args.stop_words, "r", encoding="utf-8"):
        stop_words.append(line.strip())

vectorizer = TfidfVectorizer(token_pattern="(?u)\\b\\w+\\b", stop_words=stop_words)
vecs = vectorizer.fit_transform(questions)

#for k,v in vectorizer.vocabulary_.items():
#    print(k, v)

while True:
    line = input("> ")
    if not line:
        break

    sims = cosine_similarity(vectorizer.transform([mecab.parse(line)]), vecs)
    index = np.argsort(sims[0])

    print("({:.2f}): {}".format(sims[0][index[-1]],questions[index[-1]]))
    print()
    print(answers[index[-1]])
    print()
    for i in range(2,5):
        print("({:.2f}): {}".format(sims[0][index[-i]],questions[index[-i]]))
        
    print()
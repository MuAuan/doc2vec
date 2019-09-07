from gensim.models import FastText

model=FastText.load_fasttext_format('model300.bin')


"""
#print("model.most_similar(positive=['男性','おば'], negative=['女性'])",model.most_similar(positive=['男性','おば'], negative=['女性']))
print("model.most_similar(positive=['男性','王'], negative=['女性'])",model.most_similar(positive=['男性','王'], negative=['女性']))
#print("model.most_similar(positive=['女性','王'], negative=['男性'])",model.most_similar(positive=['女性','王'], negative=['男性']))
#print("model.most_similar(positive=['フランス', '東京'], negative=['パリ'])",model.most_similar(positive=['フランス', '東京'], negative=['パリ']))
"""

print('フランス', '東京', 'パリ')
vector=model.wv['フランス']-model.wv['パリ'] +model.wv['東京']
word = model.most_similar( [ vector ], [], 10)
#print(vector)
print(word)
word = model.wv.similar_by_vector(vector, topn=10, restrict_vocab=None)
print(word)

vector = model.wv['現代の地球の支配者は人間です'] - model.wv['人間'] + model.wv['AI']
#vector = model.wv['現代の地球の支配者は人間です'] - model.wv['人間'] + model.wv['恐竜']
#vector = model.wv['現代の地球の支配者は人間です'] - model.wv['人間'] + model.wv['コンピュータ']
#vector = model.docvecs['現代の地球の支配者は人間です'] - model.wv['人間'] + model.wv['コンピュータ']
word = model.wv.similar_by_vector(vector, topn=10, restrict_vocab=None)
print(word)
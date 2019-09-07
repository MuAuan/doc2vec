from gensim import models

def sample():
    sentence = models.doc2vec.TaggedDocument(words=[u'犬', u'今日', u'吠えた'], tags=["SENT_0"])
    sentence1 = models.doc2vec.TaggedDocument(words=[u'猫', u'明日', u'吠えた'], tags=["SENT_1"])
    sentence2 = models.doc2vec.TaggedDocument(words=[u'今', u'猫', u'魚'], tags=["SENT_2"])
    sentence3 = models.doc2vec.TaggedDocument(words=[u'魚', u'泳ぐ', u'海'], tags=["SENT_3"])

    sentences = [sentence, sentence1, sentence2, sentence3]

    model = models.Doc2Vec(sentences, dm=0, vector_size=300, window=15, alpha=.025, min_alpha=.025, min_count=1, sample=1e-6)

    print('\n訓練開始')
    for epoch in range(20):
        print('Epoch: {}'.format(epoch + 1))
        model.train(sentences, epochs=model.iter, total_examples=model.corpus_count)
        model.alpha -= (0.025 - 0.0001) / 19
        model.min_alpha = model.alpha


    model.save("my_model.doc2vec")
    model_loaded = models.Doc2Vec.load('my_model.doc2vec')

    # ある文書に似ている文書を表示
    print ("SENT_0")
    print (model.docvecs.most_similar(["SENT_0"]) )
    print ("SENT_3")
    print (model.docvecs.most_similar(["SENT_3"]) )
    print ("SENT_1")
    print (model_loaded.docvecs.most_similar(["SENT_1"]) )

    # ある単語に類似した単語を取得
    print (model.similar_by_word(u"魚"))

if __name__ == '__main__':
    sample()
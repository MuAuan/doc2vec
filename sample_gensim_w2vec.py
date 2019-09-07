from gensim import models
import smart_open
import gensim

def read_corpus(fname):
    #with smart_open.smart_open(fname, encoding="utf-8") as f:
    with smart_open.open(fname, encoding="utf-8") as f:    
        for i, line in enumerate(f):
            # For training data, add tags
            yield models.doc2vec.TaggedDocument(gensim.utils.simple_preprocess(line, min_len=1), tags=["SENT_"+str(i)])

def sample():
    sentence = models.doc2vec.TaggedDocument(words=[u'犬', u'今日', u'吠えた'], tags=["SENT_0"])
    sentence1 = models.doc2vec.TaggedDocument(words=[u'猫', u'明日', u'吠えた'], tags=["SENT_1"])
    sentence2 = models.doc2vec.TaggedDocument(words=[u'今', u'猫', u'魚'], tags=["SENT_2"])
    sentence3 = models.doc2vec.TaggedDocument(words=[u'魚', u'泳ぐ', u'海'], tags=["SENT_3"])

    #sentences = [sentence, sentence1, sentence2, sentence3]

    sentences = list(read_corpus("wiki_deduct10")) #wiki_deduct_word #test_wakati.txt #jma_wakati.txt

    model = models.Doc2Vec(vector_size=200, min_count=10, epochs=1)
    #model = models.Doc2Vec(dm=0, vector_size=200, window=15, alpha=.025, min_alpha=.025, min_count=1, sample=1e-6)
    
    model.build_vocab(sentences)
    model_str="wiki10_model200_doc2vec_s"
    model.save(model_str)
    
    print('\n訓練開始')
    for epoch in range(51):
        print('Epoch: {}'.format(epoch + 1))
        model.train(sentences, epochs=model.epochs, total_examples=model.corpus_count)
        #model.alpha = 0.025 #(0.05 - 0.001) / 49
        #model.min_alpha = model.alpha
        if epoch%5==0:
            model_str="wiki10_model200_doc2vec_"+str(epoch)
            model.save(model_str)
        #model.save("wiki_model_doc2vec_0")
        #model_loaded = models.Doc2Vec.load('wiki_model_doc2vec_0')
        #model = models.Doc2Vec.load('wiki_model.doc2vec_0')

        # ある文書に似ている文書を表示
        print ("SENT_0",sentences[0][0])
        print (model.docvecs.most_similar(["SENT_0"]) )
            # ある単語に類似した単語を取得
        print("------------魚-------------------")
        print (model.similar_by_word(u"魚"))
        
    print ("SENT_3",sentences[3][0])
    print (model.docvecs.most_similar(["SENT_3"]) )
    print ("SENT_0",sentences[0][0])
    print (model.docvecs.most_similar(["SENT_0"]) )

    # ある単語に類似した単語を取得
    print("------------魚-------------------")
    print (model.similar_by_word(u"魚"))
        # ある単語に類似した単語を取得
    print("------------吠えた-------------------")
    print (model.similar_by_word(u"吠えた"))

if __name__ == '__main__':
    sample()
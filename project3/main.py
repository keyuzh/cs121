from corpus import Corpus
from lemmatization import Tokenize
from index import Index

import sys
import atexit

DEBUG = False

if __name__ == '__main__':
    path = sys.argv[1]
    corpus = Corpus(path)
    token = Tokenize()
    index = Index(corpus.get_bookkeeping())
    if not DEBUG:
        atexit.register(index.build)
    bi_gram = True


    num_fetched = 0
    if bi_gram:
        print("building bi-grams")
        index.filename = "inverted_index_bigram"
        for html in corpus.feed_html():
            fq = token.get_bi_gram_frequencies(html[0])
            num_fetched += 1
            print(num_fetched)
            # print(fq)
            index.insert(html[2], fq)
            if DEBUG and num_fetched > 10:
                break
    else:
        for html in corpus.feed_html():
            fq, pos = token.get_lemmatized_token_frequencies(html[0], bi_gram)
            num_fetched += 1
            print(num_fetched)
            # print(fq)
            index.insert(html[2], fq, pos)
    #     if num_fetched > 10:
    #         break
    #
    if DEBUG:
        index.build()



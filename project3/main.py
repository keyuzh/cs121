from corpus import Corpus
from lemmatization import Tokenize
from index import Index

import sys
import atexit


if __name__ == '__main__':
    path = sys.argv[1]
    corpus = Corpus(path)
    token = Tokenize()
    index = Index(corpus.get_bookkeeping())
    atexit.register(index.build)


    num_fetched = 0
    for html in corpus.feed_html():
        fq = token.get_lemmatized_token_frequencies(html[0])
        num_fetched += 1
        print(num_fetched)
        # print(fq)
        index.insert(html[2], fq)



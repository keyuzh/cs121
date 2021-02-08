from corpus import Corpus
from lemmatization import Tokenize

import sys


if __name__ == '__main__':
    path = sys.argv[1]
    corpus = Corpus(path)
    token = Tokenize()

    for html in corpus.feed_html():
        print(token.get_lemmatized_token_frequencies(html['content']))
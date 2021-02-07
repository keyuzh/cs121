from corpus import Corpus
from lemmatization import Tokenize

import sys


if __name__ == '__main__':
    path = sys.argv[1]
    corpus = Corpus(path)
    token = Tokenize()

    for html in corpus.feed_html():
        html_content = token.parse_html(html['content'])
        lemmatized = token.lemmatize(token.tokenize(html_content))
        print(lemmatized)
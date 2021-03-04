from corpus import Corpus
from lemmatization import Tokenize
from index import Index

import getopt, sys
import atexit

DEBUG = False

if __name__ == '__main__':
    # https://www.geeksforgeeks.org/command-line-arguments-in-python/
    # Remove 1st argument from the
    # list of command line arguments
    argumentList = sys.argv[1:]
    # Options
    options = "bc:"
    # Long options
    long_options = ["corpus =", "bigram"]
    try:
        # Parsing argument
        arguments, values = getopt.getopt(argumentList, options, long_options)
        print(arguments, values)
        # checking each argument
        for currentArgument, currentValue in arguments:
            print(currentArgument, currentValue)
    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))


    corpus_path = sys.argv[1]
    corpus = Corpus(corpus_path)
    token = Tokenize()
    index = Index(corpus.get_bookkeeping())
    if not DEBUG:
        atexit.register(index.build)
    bi_gram = False


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
            fq, pos = token.get_lemmatized_token_frequencies(html[0])
            num_fetched += 1
            print(num_fetched)
            # print(fq)
            index.insert(html[2], fq, pos)
            if DEBUG and num_fetched > 10:
                break
    #
    if DEBUG:
        index.build()



# build.py
# CS121 Winter 2021 Project 3
# Group: 6
# Name: Keyu Zhang, Chak Wah Lo, Emanuel Lopez
# UCINetID: keyuz4, cwlo1, emanuel1

"""builds the inverted index and save useful data for search"""

import atexit
import getopt
import sys

from corpus import Corpus
from index import Index
from lemmatization import Tokenize

DEFAULT_CORPUS_POSITION = "./WEBPAGES_RAW"


def parse_arguments(args) -> (str, bool):
    path = DEFAULT_CORPUS_POSITION
    bi = False
    # https://www.geeksforgeeks.org/command-line-arguments-in-python/
    # Remove 1st argument (current file) from the list of command line arguments
    argument_list = args[1:]
    # Options
    options = "bc:"
    # Long options
    long_options = ["corpus=", "bigram"]
    try:
        # Parsing argument
        arguments, values = getopt.getopt(argument_list, options, long_options)
    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))
        raise
    for arg, value in arguments:
        if arg in {"-c", "--corpus"}:
            path = value
        elif arg in {"-b", "--bigram"}:
            bi = True
    return path, bi


if __name__ == '__main__':
    # initialize objects
    corpus_path, bi_gram = parse_arguments(sys.argv)
    print(corpus_path)
    corpus = Corpus(corpus_path)
    token = Tokenize()
    index = Index(corpus.get_bookkeeping(), bi_gram)
    atexit.register(index.build)

    num_fetched = 0
    for html in corpus.feed_html():
        num_fetched += 1
        print(f"Indexing #{num_fetched}: {html[1]}")
        if bi_gram:
            fq = token.get_bi_gram_frequencies(html[0])
            index.insert(html[2], fq)
        else:
            fq, pos = token.get_lemmatized_token_frequencies(html[0])
            index.insert(html[2], fq, pos)

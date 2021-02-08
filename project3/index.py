# index.py
# CS121 Winter 2021 Project 3
# Group: 6
# Name: Keyu Zhang, Chak Wah Lo, Emanuel Lopez
# UCINetID: keyuz4, cwlo1, emanuel1

# construct inverted index with key=token, value=where the token occur; TF-IDF, etc

# Building the inverted index
# • Now that you have been provided the HTML files to index. You may build your inverted
# index off of them.
# • As most of you may already know, the inverted index is simply a map with the token as a key
# and a list of its corresponding postings.
# • A posting is nothing but the representation of the token’s occurrence in a document.
# • The posting would typically (not limited to) contain the following info (you are encouraged
# to think of other attributes that you could add to the index) :
# • The document name/id the token was found in.
# • The word frequency.
# • Indices of occurrence within the document
# • Tf-idf score etc

from collections import defaultdict

class Index:
    def __init__(self):
        # inverted_index will be a dict of sets,
        # the keys will be the tokens, values will be a set of tuples, storing the url, file path, and tf-idf score
        # {
        #     'token': set( (url, docID, tf-idf) )
        # }
        self.inverted_index = defaultdict(set)

        # container to temporarily store the word frequencies in each web page
        self.frequencies = dict()

    def insert(self, frequencies: dict):
        """"""
        pass


# lemmatization.py
# CS121 Winter 2021 Project 3
# Group: 6
# Name: Keyu Zhang, Chak Wah Lo, Emanuel Lopez
# UCINetID: keyuz4, cwlo1, emanuel1

"""
parse a html web page, fix it if its broken, tokenize the words with lemmatization,
calculate TF-IDF scores for each token,
"""

from collections import defaultdict

from lxml import html, etree
from nltk import pos_tag, tokenize
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

from project2.analytics import Analytics
from project2.project1 import WordFrequencies


def _get_stopwords(file: str):
    with open(file, 'r') as f:
        return eval(f.read())


def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    # https://www.machinelearningplus.com/nlp/lemmatization-examples-python/#wordnetlemmatizer
    tag = pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)


def get_html_object(html_content):
    if isinstance(html_content, str):
        html_content = bytes(html_content, encoding='utf8')
    return html.fromstring(html_content)


class Tokenize:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.p2_analytics = Analytics()
        self.stopword = _get_stopwords("stopwords.txt")
        self.wf = WordFrequencies()

    def tokenize(self, text: str) -> ['tokens']:
        """given a string, return a list of tokens"""
        tokens = list()
        # using default regex from https://www.nltk.org/_modules/nltk/tokenize/regexp.html
        for token in tokenize.regexp_tokenize(text, pattern=r"\w+"):
            # one letter words, punctuations, and stopwords are removed
            token = token.lower()  # convert to lower case
            if len(token) != 1 and token not in self.stopword:
                tokens.append(token)
        return tokens

    def lemmatize(self, tokens: ['tokens']) -> ['tokens']:
        """lemmatize the given token, return list of lemmatized tokens"""
        return [self.lemmatizer.lemmatize(w, get_wordnet_pos(w)) for w in tokens]

    def tokenize_and_lemmatize(self, text: str) -> ['lemmatized_tokens']:
        """convert a text string to a list of lemmatized token"""
        return self.lemmatize(self.tokenize(self.parse_html_text(text)))

    def parse_html_text(self, content: str) -> str:
        """parse html string, return text in html"""
        return self.p2_analytics._extract_text(content)

    def get_lemmatized_token_frequencies(self, html_content: str or bytes) -> ({'token': int}, {'token': {'positions'}}):
        """given a html web page in str or bytes, return a dict of token frequencies"""
        try:
            html_obj = get_html_object(html_content)
        except etree.ParserError:
            # web page cannot be parsed, treat as empty
            return dict(), dict()
        # dict to store the frequencies of tokens
        frequencies = dict()
        # first tokenize the web page as text
        all_content = self.tokenize_and_lemmatize(html_obj)
        # calculate frequencies
        self.wf.computeWordFrequencies(all_content, frequencies)
        # tokenize special tags in html
        positions = self.tag_position(html_obj)
        return frequencies, positions

    def get_bi_gram_frequencies(self, html_content: str or bytes) -> {'token': int}:
        """given a html web page in str or bytes, return a dict of token frequencies"""
        try:
            html_obj = get_html_object(html_content)
        except etree.ParserError:
            # web page cannot be parsed, treat as empty
            return dict()
        # dict to store the frequencies of tokens, bi-grams in this case
        frequencies = dict()
        # tokenize the web page as text
        all_content = self.tokenize_and_lemmatize(html_obj)
        # calculate bi-gram frequencies
        self.wf.computeWordFrequencies(all_content, frequencies, True)
        # only do frequencies and not positions in bigram, since they could have different positions
        return frequencies

    def tag_position(self, html_obj) -> {'tokens': {'positions'}}:
        """returns the html positions of all tokens"""
        positions = defaultdict(set)
        # find words in important tags, tokenize them as they have shown up multiple times in the text
        possible_pos = ['title', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'b', 'strong']
        for pos in possible_pos:
            for tag in html_obj.findall(f".//{pos}"):
                for token in self.tokenize_and_lemmatize(tag):
                    positions[token].add(pos)
        return positions

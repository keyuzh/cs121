# lemmatization.py
# CS121 Winter 2021 Project 3
# Group: 6
# Name: Keyu Zhang, Chak Wah Lo, Emanuel Lopez
# UCINetID: keyuz4, cwlo1, emanuel1

# parse a html web page, fix it if its broken, tokenize the words with lemmatization, calculate TF-IDF scores
# for each token,

# Words in title, bold and heading (h1, h2, h3) tags are more important than the other words. You should store meta-data
# about their importance to be used later in the retrieval phase.
from collections import defaultdict

from nltk import tokenize
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from project2.analytics import Analytics
from project2.project1 import WordFrequencies
from lxml import html, etree


class Tokenize:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.p2_analytics = Analytics()
        self.stopword = self._get_stopwords("stopwords.txt")
        self.wf = WordFrequencies()

    def _get_stopwords(self, file: str):
        with open(file, 'r') as f:
            return eval(f.read())

    # https: // www.machinelearningplus.com / nlp / lemmatization - examples - python /  # wordnetlemmatizer
    def get_wordnet_pos(self, word):
        """Map POS tag to first character lemmatize() accepts"""
        tag = pos_tag([word])[0][1][0].upper()
        tag_dict = {"J": wordnet.ADJ,
                    "N": wordnet.NOUN,
                    "V": wordnet.VERB,
                    "R": wordnet.ADV}
        return tag_dict.get(tag, wordnet.NOUN)

    def tokenize(self, text: str) -> ['tokens']:
        tokens = list()
        # using default regex from https://www.nltk.org/_modules/nltk/tokenize/regexp.html
        # TODO: find a better regex
        # for token in tokenize.regexp_tokenize(text, pattern=r"\w+|\$[\d\.]+|\S+"):
        for token in tokenize.regexp_tokenize(text, pattern=r"\w+"):
            # one letter words, punctuations, and stopwords are removed
            token = token.lower()
            if len(token) != 1 and token not in self.stopword:
                tokens.append(token)
        return tokens

    def lemmatize(self, tokens: ['tokens']) -> ['tokens']:
        """lemmatize the given token, return list of lemmatized tokens"""
        return [self.lemmatizer.lemmatize(w, self.get_wordnet_pos(w)) for w in tokens]

    def tokenize_and_lemmatize(self, text: str) -> ['lemmatized_tokens']:
        return self.lemmatize(self.tokenize(self.parse_html_text(text)))

    def parse_html_text(self, content: str) -> str:
        """parse html string, return text in html"""
        return self.p2_analytics._extract_text(content)

    def get_lemmatized_token_frequencies(self, html_content: str or bytes) -> ({'token': int}, {'token': {'positions'}}):
        """given a html web page in str or bytes, return a dict of token frequencies"""
        if isinstance(html_content, str):
            html_content = bytes(html_content, encoding='utf8')
        try:
            html_obj = html.fromstring(html_content)
        except etree.ParserError:
            # html.fromstring() raises this exception when the content is invalid
            # e.g. http code is not 200; content encoding is not utf-8 and cannot decode;
            #      content does not exist in corpus and therefore url_data['content'] is None;
            return dict(), dict()
        frequencies = dict()
        # first tokenize the web page as plain text
        all_content = self.tokenize_and_lemmatize(html_obj)
        self.wf.computeWordFrequencies(all_content, frequencies)
        # TODO: handle special html tags
        # tokenize special tags (again)
        positions = self.tag_position(html_obj)
        return frequencies, positions

    def get_bi_gram_frequencies(self, html_content: str or bytes) -> {'token': int}:
        """given a html web page in str or bytes, return a dict of token frequencies"""
        if isinstance(html_content, str):
            html_content = bytes(html_content, encoding='utf8')
        try:
            html_obj = html.fromstring(html_content)
        except etree.ParserError:
            # html.fromstring() raises this exception when the content is invalid
            # e.g. http code is not 200; content encoding is not utf-8 and cannot decode;
            #      content does not exist in corpus and therefore url_data['content'] is None;
            return dict()
        frequencies = dict()
        # first tokenize the web page as plain text
        all_content = self.tokenize_and_lemmatize(html_obj)
        self.wf.computeWordFrequencies(all_content, frequencies, True)
        return frequencies

    def tag_position(self, html_obj) -> {'tokens': {'positions'}}:
        """return an additional list of tokens, weights by html tags"""
        positions = defaultdict(set)
        # find words in important tags, tokenize them as they have shown up multiple times in the text
        for title in html_obj.findall('.//title'):
            for token in self.tokenize_and_lemmatize(title):
                positions[token].add('title')
        for tag in html_obj.findall('.//h1'):
            for token in self.tokenize_and_lemmatize(tag):
                positions[token].add('h1')
        for tag in html_obj.findall('.//h2'):
            for token in self.tokenize_and_lemmatize(tag):
                positions[token].add('h2')
        for tag in html_obj.findall('.//h3'):
            for token in self.tokenize_and_lemmatize(tag):
                positions[token].add('h3')
        for tag in html_obj.findall('.//h4'):
            for token in self.tokenize_and_lemmatize(tag):
                positions[token].add('h4')
        for tag in html_obj.findall('.//h5'):
            for token in self.tokenize_and_lemmatize(tag):
                positions[token].add('h5')
        for tag in html_obj.findall('.//h6'):
            for token in self.tokenize_and_lemmatize(tag):
                positions[token].add('h6')
        for tag in html_obj.findall('.//b'):
            for token in self.tokenize_and_lemmatize(tag):
                positions[token].add('b')
        for tag in html_obj.findall('.//strong'):
            for token in self.tokenize_and_lemmatize(tag):
                positions[token].add('strong')
        return positions









    # # 2. Lemmatize Single Word with the appropriate POS tag
    # word = 'feet'
    # print(lemmatizer.lemmatize(word, get_wordnet_pos(word)))
    #
    # # 3. Lemmatize a Sentence with the appropriate POS tag
    # sentence = "The striped bats are hanging on their feet for best"
    # print([lemmatizer.lemmatize(w, get_wordnet_pos(w)) for w in nltk.word_tokenize(sentence)])

# tokenize.py
# CS121 Winter 2021 Project 3
# Group: 6
# Name: Keyu Zhang, Chak Wah Lo, Emanuel Lopez
# UCINetID: keyuz4, cwlo1, emanuel1

# parse a html web page, fix it if its broken, tokenize the words with lemmatization, calculate TF-IDF scores
# for each token,

# Words in title, bold and heading (h1, h2, h3) tags are more important than the other words. You should store meta-data
# about their importance to be used later in the retrieval phase.

from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import nltk
from project2.analytics import Analytics
from lxml import html


class Tokenize:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.p2_analytics = Analytics()

    # https: // www.machinelearningplus.com / nlp / lemmatization - examples - python /  # wordnetlemmatizer
    def get_wordnet_pos(self, word):
        """Map POS tag to first character lemmatize() accepts"""
        tag = nltk.pos_tag([word])[0][1][0].upper()
        tag_dict = {"J": wordnet.ADJ,
                    "N": wordnet.NOUN,
                    "V": wordnet.VERB,
                    "R": wordnet.ADV}
        return tag_dict.get(tag, wordnet.NOUN)

    def tokenize(self, text: str) -> ['tokens']:
        tokens = nltk.tokenize.word_tokenize(text)
        # TODO: remove stop words and punctuations
        return tokens

    def lemmatize(self, tokens: ['tokens']) -> ['tokens']:
        """lemmatize the given token, return list of lemmatized tokens"""
        return [self.lemmatizer.lemmatize(w, self.get_wordnet_pos(w)) for w in tokens]

    def parse_html(self, content: str or bytes) -> str:
        """parse html string, return text in html"""
        if isinstance(content, str):
            content = bytes(content, encoding='utf8')
        html_str = html.fromstring(content)
        return self.p2_analytics._extract_text(html_str)

    # # 2. Lemmatize Single Word with the appropriate POS tag
    # word = 'feet'
    # print(lemmatizer.lemmatize(word, get_wordnet_pos(word)))
    #
    # # 3. Lemmatize a Sentence with the appropriate POS tag
    # sentence = "The striped bats are hanging on their feet for best"
    # print([lemmatizer.lemmatize(w, get_wordnet_pos(w)) for w in nltk.word_tokenize(sentence)])

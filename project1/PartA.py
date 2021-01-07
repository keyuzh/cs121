# PartA.py
# CS121 Winter 2021 Project 1
# Name: Keyu Zhang
# ID: 19898090
# UCINetID: keyuz4


############################################################################
##  PART A: Word Frequencies:                                             ##
##   Description:                                                         ##
##      Run on command line using command:                                ##
##          python PartA.py [filename]                                    ##
##   Input: [filename] - the path to a txt file                           ##
##   Output: prints tokens and frequencies                                ##
##                                                                        ##
##   Source: https://canvas.eee.uci.edu/courses/32171/assignments/623046  ##
##   (Header Uploaded by Will Schallock, last updated 1/5/21)             ##
############################################################################

import sys
from collections import defaultdict
from pathlib import Path


class WordFrequencies:
    def tokenize(self, TextFilePath: str) -> ['token']:
        """reads in a text file and returns a list of the tokens in that file.
        a token is a sequence of alphanumeric characters independent of capitalization"""
        tokens = []
        word = ''
        with open(Path(TextFilePath), encoding='utf8') as f:
            while True:
                # read one char at a time to save memory
                char = f.read(1)

                if char.isalpha() or char.isdecimal():  # accepted char for token
                    word += char.lower()  # tokens are lower case only
                elif word != '':
                    # this branch will only be triggered at the end of a token,
                    # avoid adding empty string to list of tokens when there's multiple non-alphanumeric chars in a row
                    tokens.append(word)
                    word = ''
                    
                if not char:  # end of file
                    break
        return tokens

    def computeWordFrequencies(self, tokens: ['token']) -> {'token': int}:
        """counts the number of occurrences of each token in the token list,
        returns a dict where the keys are the tokens and the values are the number of occurrences"""
        frequencies = defaultdict(int)
        for token in tokens:
            frequencies[token] += 1
        return frequencies

    def print(self, frequencies: {'token': int}):
        """prints out the word frequency counts onto the screen, ordered by decreasing frequency,
        ties are sorted alphabetically and in ascending order."""
        for k, v in sorted(frequencies.items(), key=lambda x: (-x[1], x[0])):
            print(k, '\t', v, sep='')


if __name__ == '__main__':
    wf = WordFrequencies()
    tokens = wf.tokenize(sys.argv[1])
    occurrences = wf.computeWordFrequencies(tokens)
    wf.print(occurrences)

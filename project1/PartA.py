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
from pathlib import Path
import string


class WordFrequencies:
    def tokenize(self, TextFilePath: str) -> ['token']:
        """
        reads in a text file and returns a list of the tokens in that file.
        a token is a sequence of alphanumeric characters independent of capitalization
        :argument: str representing the file path of text file
        :returns: list of lower case string 'tokens'
        :complexity: O(n) time
            while loop iterates through every char in the text file one time, so its complexity is O(n)
            all operations inside the loop are O(1)
            simplify:
                O(n) * O(1)
                -> O(n)
        """
        tokens = []
        word = ''
        with open(Path(TextFilePath), encoding='utf8') as f:
            while True:
                # read one char at a time to save memory
                char = f.read(1)

                if char in string.ascii_uppercase:
                    word += char.lower()  # tokens are lower case only
                elif (char in string.ascii_lowercase) or (char in string.digits):  # accepted char for token
                    word += char
                elif word != '':
                    # this branch will only be triggered at the end of a token,
                    # avoid adding empty string to list of tokens when there's multiple non-alphanumeric chars in a row
                    tokens.append(word)
                    word = ''
                    
                if not char:  # end of file
                    break
        return tokens

    def computeWordFrequencies(self, tokens: ['token']) -> {'token': int}:
        """
        counts the number of occurrences of each token in the token list,
        returns a dict containing the count of each token
        :argument: list of lower case string 'tokens'
        :returns: dict where the keys are str tokens and the values are int number of occurrences
        :complexity: O(n) time
            iterate through entire list of tokens, O(n)
        """
        frequencies = dict()
        for token in tokens:
            # if the key is not in dict, dict.setdefault method initiates the value at 0
            frequencies[token] = frequencies.setdefault(token, 0) + 1
        return frequencies

    def print(self, frequencies: {'token': int}) -> None:
        """
        prints out the word frequency counts onto the screen, ordered by decreasing frequency,
        ties are sorted alphabetically and in ascending order.
        :argument: dict where the keys are str tokens and the values are int number of occurrences
        :returns: None
        :complexity: O(n log n) time due to sorting; O(n) excluding sort
            sorting the keys in dict takes O(n log n) time
            then iterate through the sorted key-value pairs, O(n)
            simplify:
                O(n log n) + O(n)
                -> O(n log n)
        """
        for k, v in sorted(frequencies.items(), key=lambda x: (-x[1], x[0])):
            print(k, '\t', v, sep='')


def main():
    """
    given path to a text file from terminal; tokenize the text in the file and
    :return:
    """
    wf = WordFrequencies()
    tokens = wf.tokenize(sys.argv[1])
    occurrences = wf.computeWordFrequencies(tokens)
    wf.print(occurrences)


if __name__ == '__main__':
    main()

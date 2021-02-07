# PartA.py
# CS121 Winter 2021 Project 1
# Name: Keyu Zhang
# ID: 19898090
# UCINetID: keyuz4

# modified version of project 1 - Part A for use in project 2

import string
import sys


class WordFrequencies:
    def tokenize(self, text: str) -> ['token']:
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
        # project2: takes a str to tokenize instead of a text file
        tokens = []
        word = ''
        for char in text:
            # read one char at a time to save memory
            if char in string.ascii_uppercase:
                word += char.lower()  # tokens are lower case only
            elif (char in string.ascii_lowercase) or (char in string.digits):  # accepted char for token
                word += char
            elif word != '':
                # this branch will only be triggered at the end of a token,
                # avoid adding empty string to list of tokens when there's multiple non-alphanumeric chars in a row
                tokens.append(word)
                word = ''
        return tokens

    def computeWordFrequencies(self, tokens: ['token'], frequencies: {'token': int}, stopwords: {str}):
        """
        counts the number of occurrences of each token in the token list,
        returns a dict containing the count of each token
        :argument: list of lower case string 'tokens'
        :returns: dict where the keys are str tokens and the values are int number of occurrences
        :complexity: O(n) time
            iterate through entire list of tokens, O(n)
        """
        # project2: update this method to take existing dict as parameter and modify it
        #           additionally, stopwords are not inserted in the dict;
        #           words shorter than 3 character or contains all digits are ignored
        for token in tokens:
            # if the key is not in dict, dict.setdefault method initiates the value at 0
            if token not in stopwords and len(token) >= 3 and not token.isdigit():
                frequencies[token] = frequencies.setdefault(token, 0) + 1

    def print(self, frequencies: {'token': int}) -> [str]:
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
        # project2: return the key-value pairs as a list of str instead of print to console
        return [f"{k}\t{v}" for k, v in sorted(frequencies.items(), key=lambda x: (-x[1], x[0]))]
        # sort first by value in decreasing order, then by key in alphabetical order


def main():
    """
    given path to a text file from terminal; tokenize the text in the file, count the number of tokens,
    and print tokens and its count in sorted order into the terminal
    :return: None
    :complexity: O(n log n) including sort; O(n) excluding sort
    """
    wf = WordFrequencies()
    tokens = wf.tokenize(sys.argv[1])
    occurrences = wf.computeWordFrequencies(tokens)
    wf.print(occurrences)


if __name__ == '__main__':
    main()

# 1. Keep track of the subdomains that it visited, and count how many different URLs it has
# processed from each of those subdomains.
# 2. Find the page with the most valid out links (of all pages given to your crawler). Out Links are the
# number of links that are present on a particular webpage.
# 3. List of downloaded URLs and identified traps.
# 4. What is the longest page in terms of number of words? (HTML markup doesn’t count as words)
# 5. What are the 50 most common words in the entire set of pages? (Ignore English stop words,
# which can be found, (https://www.ranks.nl/stopwords)

from project1 import WordFrequencies

class Analytics:
    def __init__(self):
        self.wf = WordFrequencies()

        self.crawlHistory = {} #Dictionary to story crawl history
        self.traps = [] #list that story all the known traps url
        self.most_valid_links = 0
        self.most_valid_page = None
        # tuple containing the url of the page with the most words and the number of words
        self.longest_page = (None, 0)

    def _write(self, file: open, line: str):
        # use this method to write to file so you can forget \n
        file.write(line + '\n')

    def write_crawl_history(self):
    #
        with open("crawl_history.txt", "w") as f:
            for key, value in self.crawlHistory.items():
                f.write(f"{key:<30}{value:>10}\n")

    def write_most_valid_page(self):
        # update format
        with open("most_valid_page.txt", "w") as f:
            self._write(f, "Page with the most valid out links:")
            self._write(f, str(self.most_valid_page))
            self._write(f, "Number of out links:")
            self._write(f, str(self.most_valid_links))

    def write_url_traps(self):
        #
        with open("url_and_traps.txt", "w") as f:
            f.write("url:\n")
            for key in self.crawlHistory.keys():
                f.write("  " + key + "\n")

            f.write("\nTraps:\n")
            for item in self.traps:
                f.write("  " + item + "\n")

    def write_longest_page(self):
        with open("longest_page.txt", 'w') as f:
            self._write(f, "Longest page in terms of number of words:")
            self._write(f, str(self.longest_page[0]))
            self._write(f, "Number of words:")
            self._write(f, str(self.longest_page[1]))

    def write_all(self):
        self.write_crawl_history()
        self.write_most_valid_page()
        self.write_url_traps()
        self.write_longest_page()

    def update_most_valid_links(self, url: str, count: int):
        if count > self.most_valid_links:
            self.most_valid_links = count
            self.most_valid_page = url

    def count_words(self, url: str, text: str):
        # use tokenize() method from project1
        num_of_words = len(self.wf.tokenize(text))
        if num_of_words > self.longest_page[1]:
            self.longest_page = (url, num_of_words)

# 1. Keep track of the subdomains that it visited, and count how many different URLs it has
# processed from each of those subdomains.
# 2. Find the page with the most valid out links (of all pages given to your crawler). Out Links are the
# number of links that are present on a particular webpage.
# 3. List of downloaded URLs and identified traps.
# 4. What is the longest page in terms of number of words? (HTML markup doesn’t count as words)
# 5. What are the 50 most common words in the entire set of pages? (Ignore English stop words,
# which can be found, (https://www.ranks.nl/stopwords)

class Analytics:
    def __init__(self):

        self.crawlHistory = {} #Dictionary to story crawl history
        self.traps = [] #list that story all the known traps url
        self.most_valid_links = 0 #
        self.most_valid_page = None #

    def write_crawl_history(self):
    #
        with open("crawl_history.txt", "w") as f:
            for key, value in self.crawlerHistory.items():
                f.write(f"{key:<30}{value:>10}\n")

    def write_most_valid_page(self):
        #
        with open("most_valid_page.txt", "w") as f:
            f.write(self.most_valid_page)

    def write_url_traps(self):
        #
        with open("url_and_traps.txt", "w") as f:
            f.write("url:\n")
            for key in self.crawlHistory.keys():
                f.write(key + "\n")

            f.write("\nTraps:\n")
            for item in self.traps:
                f.write(item + "\n")
                
            

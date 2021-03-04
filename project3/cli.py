import time

from corpus import Corpus


class CLI:
    def __init__(self, search, corpus_path):
        self.search = search
        self.corpus = Corpus(corpus_path)

    def start_search(self, query):
        start = time.time()
        num_results, urls = self.search.search(query, 20)
        search_time = time.time() - start
        # show results
        self.display_results(query, [i[0] for i in urls], num_results, search_time)

    def display_results(self, query, paths, num_results, search_time):
        print()
        print(f"{query}: {num_results} results ({search_time:.4f} seconds)")
        print(f"Showing top {min(20, num_results)} results")
        print()

        for index, path in enumerate(paths):
            num = index + 1
            title = self.corpus.get_title(path)
            print(f"#{num}: {title}")
            print(self.corpus.get_url(path))
            print()

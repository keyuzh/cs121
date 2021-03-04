import json
import sys
from pathlib import Path

import lxml.html


class Corpus:
    def __init__(self, corpus_path: str or Path):
        if isinstance(corpus_path, str):
            corpus_path = Path(corpus_path)
        self.path = corpus_path
        self.bookkeeping = self._json_to_dict(self.path / "bookkeeping.json")

    def _json_to_dict(self, json_path: Path) -> dict:
        with open(json_path, encoding='utf8') as json_file:
            return json.load(json_file)


    def feed_html(self) -> dict:
        """iterator that yields html from local corpus"""
        for path, url in self.bookkeeping.items():
            html_content = self.get_html(path)
            yield (html_content, url, path)

    def get_html(self, path: str) -> str:
        with self.get_file(path) as f:
            return f.read()

    def get_file(self, path) -> open:
        path_list = path.split('/')
        directory = path_list[0]
        file = path_list[1]
        file_path = self.path / directory / file
        return open(file_path, encoding='utf8')


    def get_bookkeeping(self):
        return self.bookkeeping

    def get_url(self, path: str) -> str:
        """get the url of the webpage given the path"""
        return self.bookkeeping[path]

    def get_title(self, path: str) -> str:
        #https://stackoverflow.com/questions/51233/how-can-i-retrieve-the-page-title-of-a-webpage-using-python
        t = lxml.html.parse(self.get_file(path))
        try:
            return t.find(".//title").text
        except:
            return "(Description not found)"

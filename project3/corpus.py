import json
import sys
from pathlib import Path



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
            # split key by /
            path = path.split('/')
            directory = path[0]
            file = path[1]
            file_path = self.path / directory / file
            with open(file_path, encoding='utf8') as f:
                html_content = f.read()
            yield (html_content, url)

import random
from pathlib import Path
import os


WORDS = ['a', 'b', 'c', 'd', 'e']

def main():
    num_words = int(input("number of words(in thousands) in file: ")) * 1000
    try:
        os.mkdir("text")
    except FileExistsError:
        pass

    file_path = Path(".") / Path('text') / Path(f"{int(num_words / 1000)}Kwords.txt")
    f = open(file_path, 'w')
    for i in range(num_words):
        word = ''.join([random.choice(WORDS) for _ in range(5)]) + '\n'
        f.write(word)
    f.close()

if __name__ == '__main__':
    main()

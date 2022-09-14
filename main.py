import numpy as np
import re
from functools import lru_cache
import time

with open("words3000.txt", "r") as file:
    contents = file.read()
    words = contents.strip().split("\n")
    words_by_length = {i: [] for i in set([len(word) for word in words])}

    np.random.shuffle(words)

    for word in words:
        words_by_length[len(word)].append(word.upper())


@lru_cache(maxsize=None)
def get_available_words(letter_array):
    if all([i == " " for i in letter_array]):
        return words_by_length[len(letter_array)]

    pattern = r"^"
    for letter in letter_array:
        if letter == " ":
            pattern += r"\w"
        else:
            pattern += letter.lower()

    pattern += r"$"
    available = []
    for word in words:
        if re.match(pattern, word):
            available.append(word)
    return tuple(available)


class Crossword:
    def __init__(self, template, repeat_words=True):
        template = np.array([list(row) for row in template])
        self.grid = template
        self.shape = template.shape
        self.repeat = repeat_words
        self.words = []

        self.acrosses = self.get_acrosses()
        self.downs = self.get_downs()
        self.total_solutions = 0
        self.nodes_searched = 0

    def __str__(self):
        string = ''
        for row in self.grid:
            string += '|'
            string += '|'.join(row).replace('#', ' ')
            string += '|'
            string += "\n"
        return string

    def get_acrosses(self):
        row = 0

        acrosses = []
        while row < self.shape[0]:
            col = 0

            while col < self.shape[1]:
                across = []
                length = 0
                start_row = row
                start_col = col
                while col < self.shape[1] and self.grid[row, col] != "#":
                    across.append(self.grid[row, col])
                    col += 1
                    length += 1
                col += 1

                if length > 1:
                    acrosses.append((start_row, start_col, across))

            row += 1
        return acrosses

    def get_downs(self):
        col = 0

        downs = []
        while col < self.shape[1]:
            row = 0

            while row < self.shape[0]:
                down = []
                length = 0
                start_row = row
                start_col = col
                while row < self.shape[0] and self.grid[row, col] != "#":
                    down.append(self.grid[row, col])
                    row += 1
                    length += 1
                row += 1

                if length > 1:
                    downs.append((start_row, start_col, down))

            col += 1
        return downs

    def fit_crossword(self):
        self.acrosses = self.get_acrosses()
        self.downs = self.get_downs()
        self.nodes_searched += 1

        # Check if crossword has empty cells
        string = '#'.join([''.join(row) for row in self.grid])
        if " " not in string:
            # Check all words in crossword are in word bank
            for word in self.downs + self.acrosses:
                if ''.join(word[2]) not in words_by_length[len(word[2])]:
                    return
            return True

        # Find unfilled across words with smallest number of available words
        min_across_available_num = float("+inf")
        min_across = self.acrosses[0]
        min_across_available_words = []
        for across in self.acrosses:
            if " " not in across[2]:
                continue

            # Get available words for current unfilled word
            available_words = get_available_words(tuple(across[2]))
            # If no words can be filled into an unfilled word, return
            if len(available_words) == 0:
                return

            # Find unfilled words with smallest number of available words
            if len(available_words) < min_across_available_num:
                min_across_available_num = len(available_words)
                min_across = across
                min_across_available_words = available_words

        # Find unfilled down words with smallest number of available words
        min_down_available_num = float("+inf")
        min_down = self.downs[0]
        min_down_available_words = []
        for down in self.downs:
            if " " not in down[2]:
                continue

            # Get available words for current unfilled word
            available_words = get_available_words(tuple(down[2]))
            # If no words can be filled into an unfilled word, return
            if len(available_words) == 0:
                return

            # Find unfilled down words with smallest number of available words
            if len(available_words) < min_down_available_num:
                min_down_available_num = len(available_words)
                min_down = down
                min_down_available_words = available_words

        if min_across_available_num < min_down_available_num:
            for word in min_across_available_words:
                word = word.upper()
                if not self.repeat and word in self.words:
                    continue

                self.words.append(word)
                for i in range(len(min_across[2])):
                    if min_across[2][i] == " ":
                        self.grid[min_across[0], min_across[1] + i] = word[i]

                if self.fit_crossword():
                    return True

                self.words.pop()
                for i in range(len(min_across[2])):
                    if min_across[2][i] == " ":
                        self.grid[min_across[0], min_across[1] + i] = " "
        else:
            for word in min_down_available_words:
                word = word.upper()
                if not self.repeat and word in self.words:
                    continue

                self.words.append(word)
                for i in range(len(min_down[2])):
                    if min_down[2][i] == " ":
                        self.grid[min_down[0] + i, min_down[1]] = word[i]

                if self.fit_crossword():
                    return True

                self.words.pop()
                for i in range(len(min_down[2])):
                    if min_down[2][i] == " ":
                        self.grid[min_down[0] + i, min_down[1]] = " "


if __name__ == "__main__":
    crossword_template = ["     #     ",
                          " ### # # # ",
                          "   #       ",
                          " # # # # # ",
                          "#     #    ",
                          " # # # # # ",
                          "    #     #",
                          " # # # # # ",
                          "       #   ",
                          " # # # ### ",
                          "     #     "]


    crossword = Crossword(crossword_template, repeat_words=False)

    start = time.time()
    result = crossword.fit_crossword()
    end = time.time()

    hits, misses = get_available_words.cache_info()[:2]

    if result:
        print(crossword)
    else:
        print("CROSSWORD NOT POSSIBLE WITH CURRENT WORD BANK")
    print(f"NODES SEARCHED: {crossword.nodes_searched}")
    print(f"WORD BANK SEARCHED: {misses}")
    print(f"TIME TAKEN: {end - start:.4f}s")
    print()
    print(crossword.words)

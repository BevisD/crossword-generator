import numpy as np
import re

with open("words3000.txt", "r") as file:
    contents = file.read()
    words = contents.strip().split("\n")
    words_by_length = {i: [] for i in set([len(word) for word in words])}

    np.random.shuffle(words)

    for word in words:
        words_by_length[len(word)].append(word.upper())


def get_available_words(letter_array):
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
    return available


class Crossword:
    def __init__(self, template):
        template = np.array([list(row) for row in template])
        self.grid = template
        self.shape = template.shape

        self.acrosses = self.get_acrosses()
        self.downs = self.get_downs()
        self.total_solutions = 0
        self.first_word = ''

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

        string = '#'.join([''.join(row) for row in self.grid])
        if " " not in string:
            for word in self.downs + self.acrosses:

                if ''.join(word[2]) not in words_by_length[len(word[2])]:
                    return
            return True

        min_across_available_num = float("+inf")
        min_across = self.acrosses[0]
        min_across_available_words = []
        for across in self.acrosses:
            if " " not in across[2]:
                continue

            available_words = get_available_words(across[2])
            if len(available_words) < min_across_available_num:
                min_across_available_num = len(available_words)
                min_across = across
                min_across_available_words = available_words

        min_down_available_num = float("+inf")
        min_down = self.downs[0]
        min_down_available_words = []
        for down in self.downs:
            if " " not in down[2]:
                continue
            available_words = get_available_words(down[2])
            if len(available_words) < min_down_available_num:
                min_down_available_num = len(available_words)
                min_down = down
                min_down_available_words = available_words

        if min_across_available_num < min_down_available_num:
            for word in min_across_available_words:
                for i in range(len(min_across[2])):
                    if min_across[2][i] == " ":
                        self.grid[min_across[0], min_across[1] + i] = word[i].upper()
                if self.fit_crossword():
                    return True

                for i in range(len(min_across[2])):
                    if min_across[2][i] == " ":
                        self.grid[min_across[0], min_across[1] + i] = " "
        else:
            for word in min_down_available_words:
                for i in range(len(min_down[2])):
                    if min_down[2][i] == " ":
                        self.grid[min_down[0] + i, min_down[1]] = word[i].upper()

                if self.fit_crossword():
                    return True

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

    crossword = Crossword(crossword_template)
    crossword.fit_crossword()
    print(crossword)

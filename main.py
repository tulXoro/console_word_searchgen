from random import randint, shuffle

from typing import Tuple, Callable

import logging

logging.basicConfig(level=0, filename="wordsearch.log", filemode="w", format='%(levelname)s: %(message)s')

with open("wordlist.txt") as file:
    word_list = file.readlines()

# format word_list
word_list = [s.strip('\n') for s in word_list]
shuffle(word_list)

board = []
answer_key = []
alphabet = "abcdefghijklmnopqrstuvwxyz"
alphabet = list(alphabet)
word_dict = {}
tries = 50

board_len = input("Please input how big the board should be: ")
while True:
    try:
        board_len = int(board_len)
        break
    except ValueError:
        board_len = input("Invalid value... Try again: ")
        logging.exception(f"Invalid value entered for board length ({board_len})")

logging.info(f"Value ({board_len}) has been set as board length")

# Randomly add letters into the board
for i in range(board_len):
    row = []
    answer_row = []
    for j in range(board_len):
        row.append(alphabet[randint(0, len(alphabet) - 1)])
        answer_row.append("*")
    board.append(row)
    answer_key.append(answer_row)

logging.info(f"Added random letters to row...")


def insert_word(x, y, word, direction):
    direction_func = {
        "row": (lambda i: (i, 0)),
        "col": (lambda i: (0, i)),
        "diagbl": (lambda i: (i, i)),
        "diagtl": (lambda i: (i, -i))
    }.get(direction)

    if direction_func is None:
        return

    for j, char in enumerate(word):
        dx, dy = direction_func(j)
        new_y, new_x = y + dy, x + dx
        logging.info(rf"Adding word '{word}' at ({x},{y}) on ({new_x},{new_y}) facing {direction}")
        # Insert char at (new_y, new_x)
        board[new_y][new_x] = char
        answer_key[new_y][new_x] = char
        word_dict[(new_y, new_x)] = word


def add_words():
    global board
    for word in word_list:
        if len(word) > board_len:
            print(f"Word {word} is too large! Skipping...")
            logging.critical(f"Word {word} is too large! Skipping...")
            continue

        attempts = 50
        # horizontal, vertical or diagonal
        orientation = randint(0, 3)

        place_x, place_y = random_placement(word)

        # reverse
        if randint(0, 4) == 0 or (orientation == 3 and randint(0, 4) <= 3):
            word = word[::-1]

        logging.info(f"Adding \"{word}\" at attempt {attempts} with orientation {orientation}")

        # horizontal
        if orientation == 0:
            place_x = bound(word, True, False)

            conflict = False
            while True:
                for j in range(len(word)):
                    if word_dict.get((place_y, place_x + j)) is not None and board[place_y][place_x + j] != word[j]:
                        place_x, place_y = random_placement(word)
                        place_x = bound(word, True, False)
                        conflict = True
                        if attempts <= 0:
                            logging.error(f"Failed to add \"{word}\" after 50 tries")
                            return -1
                        attempts -= 1
                        break
                if not conflict:
                    break

            # add word
            insert_word(place_x, place_y, word, "row")
        # vertical
        elif orientation == 1:
            place_y = bound(word, False, True)

            conflict = False
            while True:
                for j in range(len(word)):
                    if word_dict.get((place_y + j, place_x)) is not None and board[place_y + j][place_x] != word[j]:
                        place_x, place_y = random_placement(word)
                        place_y = bound(word, False, True)
                        conflict = True
                        if attempts <= 0:
                            logging.error(f"Failed to add \"{word}\" after 50 tries")
                            return -1
                        attempts -= 1
                        break
                if not conflict:
                    break

            # add word
            insert_word(place_x, place_y, word, "col")

        # diagonal top-left
        elif orientation == 2:
            place_x, place_y = bound(word, True, True)

            conflict = False
            while True:
                for j in range(len(word)):
                    if word_dict.get((place_y + j, place_x + j)) is not None and board[place_y + j][place_x + j] != \
                            word[j]:
                        place_y, place_x = bound(word, True, True)
                        conflict = True
                        if attempts <= 0:
                            logging.error(f"Failed to add \"{word}\" after 50 tries")
                            return -1
                        attempts -= 1
                        break
                if not conflict:
                    break

                    # add word
            insert_word(place_x, place_y, word, "diagbl")
        # diagonal bot-left
        else:
            place_x = bound(word, True)
            place_y = randint(len(word) - 1, board_len - 1)

            conflict = False
            while True:
                for j in range(len(word)):
                    if word_dict.get((place_y - j, place_x + j)) is not None and board[place_y - j][place_x + j] != \
                            word[j]:
                        place_x = bound(word, True)
                        place_y = randint(len(word) - 1, board_len - 1)
                        conflict = True
                        if attempts <= 0:
                            logging.error(f"Failed to add \"{word}\" after 50 tries")
                            return -1
                        attempts -= 1
                        break
                if not conflict:
                    break

            # add word
            insert_word(place_x, place_y, word, "diagtl")
    return 0


# randomly select a spot to place word
def random_placement(word: str) -> Tuple[int, int]:
    # pick an x and y value
    placement_x = randint(0, board_len - 1)
    placement_y = randint(0, board_len - 1)
    while placement_x + (len(word) - 1) > board_len:
        placement_x = randint(0, board_len - 1)
    while placement_y + (len(word) - 1) > board_len:
        placement_y = randint(0, board_len - 1)
    return placement_x, placement_y


# Make sure words stay in the bounds of the grid
def bound(word, x=False, y=False):
    place_x = randint(0, board_len - len(word) - 1)
    place_y = randint(0, board_len - len(word) - 1)
    if x and y:
        return place_x, place_y
    elif x:
        return place_x
    return place_y


while tries > 0:
    if add_words() != 0:
        tries -= 1
        print(f"Failed to add words... Trying again")
        logging.error(f"Failed to add words with {tries} tries")
    else:
        break

if tries == 0:
    print(f"Failed to generate words. Max number of attempts have exceeded.")
    logging.critical("Failed to add words after 50 tries...")
    exit(-1)

# Export to a different file
with open("output.txt", "w") as file:
    out_str = ""
    for row in board:
        out_str += " ".join(row) + "\n"
    file.write(out_str)
    logging.info("Generated output file.")

with open("answer_key.txt", "w") as file:
    out_str = ""
    for row in answer_key:
        out_str += " ".join(row) + "\n"
    file.write(out_str)
    logging.info("Generated answer key file.")

logging.info(f"Completed with {tries} tries remaining.")
print("Completed. Please check answer_key.txt and output.txt")

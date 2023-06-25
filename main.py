from random import randint, shuffle

from typing import Tuple

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

# board_len = input("Please input how big the board should be: ")
board_len = 10
flag = True

# Make sure input is a string
while flag:
    try:
        board_len = int(board_len)
        flag = False
    except ValueError:
        board_len = input("Please input a number. Try again: ")

# Randomly add letters into the board
for i in range(board_len):
    row = []
    answer_row = []
    for j in range(board_len):
        row.append(alphabet[randint(0, len(alphabet)-1)])
        answer_row.append("*")
    board.append(row)
    answer_key.append(answer_row)

# Add the words
# for i, row in enumerate(board):
#     for j, col in enumerate(row):
def add_words():
    global board
    for word in word_list:
        attempts = 50
        # horizontal, vertical or diagonal
        orientation = randint(0, 1)

        print(f"\n\nword check: {word}")
        place_x, place_y = random_placement(word)

        # # reverse
        # if randint(0, 4) == 0:
        #     word = word[::-1]
        #     print(f"{word} is reversed!")

        # horizontal
        if orientation == 0:
            place_x = bound(word, True, False)

            conflict = False
            while True:
                for j in range(place_x, place_x+len(word)):
                    if word_dict.get((place_y, j)) is not None and board[place_y][j] != word[j-place_x]:
                        print(f"conflict found with {word} and {word_dict.get((place_y, j))} with {attempts}")
                        print(f"COORDS: y:{place_y} x:{place_x}")
                        place_x, place_y = random_placement(word)
                        place_x = bound(word, True, False)
                        conflict = True
                        if attempts <= 0:
                            print(f"failed to add {word} after 50 tries")
                            return -1
                        attempts -= 1
                        break
                if conflict:
                    conflict = False
                    continue

                break

            # add word
            for j, chars in enumerate(word):
                board[place_y][place_x+j] = chars
                answer_key[place_y][place_x+j] = chars
                word_dict[(place_y, place_x+j)] = word
            print(f"added word {word} at y:{place_y} x:{place_x}")

        elif orientation == 1:
            place_y = bound(word, False, True)

            conflict = False
            while True:
                for j in range(place_y, place_y+len(word)):
                    if word_dict.get((j, place_x)) is not None and board[j][place_x] != word[j-place_y]:
                        print(f"conflict found with {word} and {word_dict.get((j, place_x))} with {attempts}")
                        print(f"COORDS: y:{place_y} x:{place_x}")
                        place_x, place_y = random_placement(word)
                        place_y = bound(word, False, True)
                        conflict = True
                        if attempts <= 0:
                            print(f"failed to add {word} after 50 tries")
                            return -1
                        attempts -= 1
                        break
                if conflict:
                    conflict = False
                    continue
                break

            # add word
            for j, chars in enumerate(word):
                board[place_y + j][place_x] = chars
                answer_key[place_y + j][place_x] = chars
                word_dict[(place_y + j, place_x)] = word
            print(f"added word {word} at y:{place_y} x:{place_x}")
    return 0


def random_placement(word: str) -> Tuple[int, int]:
    # pick an x and y value
    placement_x = randint(0, board_len - 1)
    placement_y = randint(0, board_len - 1)
    while placement_x + (len(word) - 1) > board_len:
        placement_x = randint(0, board_len - 1)
    while placement_y + (len(word) - 1) > board_len:
        placement_y = randint(0, board_len - 1)
    return placement_x, placement_y

def bound(word, x=False, y=False):
    place_x = randint(0, board_len - len(word) - 1)
    place_y = randint(0, board_len - len(word) - 1)
    if x and y:
        return (place_x, place_y)
    elif x:
        return place_x
    return place_y

print(word_list)

while tries > 0:
    if add_words() != 0:
        tries -= 1
        print(f"failed to add words... trying again")
    else:
        break


if tries == 0:
    print(f"exit with 0 tries")
    exit(-1)

# Export to a different file
with open("output.txt", "w") as file:
    out_str = ""
    for row in board:
        out_str += " ".join(row) + "\n"
    file.write(out_str)

with open("answer_key.txt", "w") as file:
    out_str = ""
    for row in answer_key:
        out_str += " ".join(row) + "\n"
    file.write(out_str)

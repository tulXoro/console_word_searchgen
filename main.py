from random import randint, shuffle

with open("wordlist.txt") as file:
    word_list = file.readlines()

# format word_list
word_list = [s.strip('\n') for s in word_list]
shuffle(word_list)

board = []
alphabet = "abcdefghijklmnopqrstuvwxyz"
alphabet = list(alphabet)

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
    for j in range(board_len):
        row.append(alphabet[randint(0, len(alphabet)-1)])
    board.append(row)


# Add the words
# for i, row in enumerate(board):
#     for j, col in enumerate(row):
def add_words():
    global board
    # we will decide if we want to add words by row
    for i, row in enumerate(board):
        for j, col in enumerate(row):
            print (col)


# Export to a different file
with open("output.txt", "w") as file:
    out_str = ""
    for row in board:
        out_str += " ".join(row) + "\n"
    file.write(out_str)

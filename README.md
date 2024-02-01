# Description
This is a simple application that generates a wordsearch. I built this to primarily help children and teens learn about the fundamentals of programming.

# Usage
You may use this project however you see fit.

# How to start
Ensure you have [Python](https://www.python.org/downloads/) installed, and optionally use an IDE. Clone the repository and run the game with `python3 main.py`. Add words into `wordlist.txt` and run the program. 

# How to use
Enter the size of the board and wait for a few seconds. There will be an output file called `output.txt` which shows the generated board. There will also be another file `answer_key.txt` that shows where every word is placed in the board. If the board is too small or there are too many words, the program may fail.

# How it works
It works by generating a random position to place each word. It tries this multiple times until it can place that word.

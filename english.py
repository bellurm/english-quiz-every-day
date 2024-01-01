import random
import sqlite3
import os, sys

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def read_words_from_file(file_name):
    words = {}
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            words = dict(line.strip().split(":") for line in file)
    except FileNotFoundError:
        print(f"{RED}[WARN] The file is not exists. Please, enter a valid file name.{RESET}")
    return words

def read_asked_words_from_db(database):
    asked_words = set()
    try:
        with sqlite3.connect(database) as connection:
            cursor = connection.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS AskedWords(Word TEXT PRIMARY KEY);")
            cursor.execute("SELECT Word FROM AskedWords;")
            asked_words = set(row[0] for row in cursor.fetchall())
    except sqlite3.Error as e:
        print(f"{RED}[WARN] Can not connect to the database.{RESET}")
    return asked_words


def ask_word(word, correct_answer):
    
    while True:
        answer = input(f"{YELLOW}'{word}' >>> {RESET}").strip().lower()
        if answer == correct_answer:
            print(f"{GREEN}[INFO] Correct!{RESET}")
            return True
        else:
            print(f"{RED}[INFO] Wrong! Try it again.{RESET}")
        
def add_word_to_db(word, database):
    try:
        with sqlite3.connect(database) as connection:
            connection.execute("INSERT INTO AskedWords (Word) VALUES (?);", (word,))
    except sqlite3.Error as e:
        print(f"{RED}[WARN] Can not connect to the database.{RESET}")

def main():

    def usage():
        usage = f"{BLUE}[USAGE]\nusage1: python english.py\nusage2: python english.py --clear-db{RESET}"
        print(usage)
        return exit(0)
    
    file_name = "words.txt"
    database = "asked_words.db"

    if len(sys.argv) == 2 and sys.argv[1] == "--clear-db":
        os.remove(database)
        print(f"{GREEN}[INFO] The database is removed. If you run the program again, a new database comes up.{RESET}")
        exit(0)
    elif len(sys.argv) == 2 and sys.argv[1] != str("--clear-db"):
        usage()
    elif len(sys.argv) > 2:
        usage()
    else:
        pass
    
    words = read_words_from_file(file_name)
    if not words:
        return

    asked_words = read_asked_words_from_db(database)

    correct_answers = 0
    words_to_ask = set(words.keys()) - asked_words

    if not words_to_ask:
        print(f"{BLUE}[WARN] There is no word to ask. Please add more.{RESET}")
        os.remove(database)
                
        return f"{GREEN}[CONGRATS] Congrats, You finished 'em all!\n[INFO] The database is removed. If you run the program again, a new database comes up.{RESET}"

    for _ in range(min(3, len(words_to_ask))):
        word = random.choice(list(words_to_ask))
        correct_answer = words[word]
        try:
            if ask_word(word, correct_answer):
                add_word_to_db(word, database)
                correct_answers += 1
        except KeyboardInterrupt:
            print(f"{BLUE}[INFO] Quitted by user.{RESET}")
            exit(0)
        except UnboundLocalError:
            pass

    print(f"{GREEN}[INFO] Total number correct: {correct_answers}/{len(words_to_ask)}{RESET}")

if __name__ == "__main__":
    main()

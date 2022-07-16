import os

from numpy import true_divide


def create_word_list(length):
    # takes all English words (https://github.com/dwyl/english-words)
    with open('EnglishWords.txt') as wordsFile:
        # a set is made, so that no words appear twice
        allWords = set(wordsFile.read().split())
        # filters all the words with a specific length
        validWords = {word for word in allWords if len(word) == length}

    if length == 5:  # The official Wordle game has some words that are not on the main list
        # the Wordle word list is taken from the source code of the game, which is publicly available
        with open('WordleWords.txt') as wordsFile:
            wordleWords = set(wordsFile.read().split())  # makes another set
            validWords.update(wordleWords)  # we update the main set

    # the final set is returned, ordered alphabetically
    return sorted(validWords)


def get_int(message, maximum):
    while True:
        print(message, end='')
        raw = input()
        if raw.isnumeric():
            raw = int(raw)
            if raw <= maximum or maximum == 0:
                return raw
        print('Invalid input')


def get_char(message, single):
    while True:
        print(message, end='')
        raw = input()
        if raw == '':
            return raw
        if raw.isalpha():
            raw = raw.lower()
            if single == True:
                if len(raw) < 2:
                    return raw
            else:
                return raw
        print('Invalid input')


def positional_check(set_to_check, positions_list, length):
    for element in set_to_check:
        position = get_int(
            f'What position did you check "{element}" on? ', length)
        positions_list[position-1].append(element)


def add_input_to_set(main_set: set, message: str=''):
    string = get_char(message, False)
    aux_set = set()
    for character in string:
        aux_set.add(character)
    main_set.update(aux_set)


def continue_check():
    while True:
        check = input("Restart? [Yes/ No] ")
        if check in ('Yes', 'Y', 'yes', 'y', '1'):
            return True
        if check in ('No', 'N', 'no', 'n', '0'):
            return False


def clear_screen():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')


def check_known(word: str, known: list):
    """Checks if the word has all the known letters in their positions."""
    for i, known_letter in enumerate(known):
        if known_letter and known_letter != word[i]:
            return False
    return True


def check_not_contained(word: str, not_contained: list, contained: list, positions_to_check: list):
    """Checks if the word contains all the letters with unknown positions."""
    for character in not_contained:
        if character not in contained:
            for i in positions_to_check:
                if character == word[i]:
                    return False
    return True


def check_contained(word: str, contained: list, positions_to_check: list, tried: list):
    is_contained = True
    for character in contained:
        is_contained = False
        for i in positions_to_check:
            if character == word[i]:
                if character not in tried[i]:
                    is_contained = True
        if is_contained == False:
            return False
    return True


def guess():
    clear_screen()
    length = get_int('Word length: ', 0)
    possibilities = create_word_list(length)
    known = list()
    positions_to_check = list()
    for i in range(length):
        known.append('')
        positions_to_check.append(i)
    contained = set()
    not_contained = set()
    # letters tried for every position, as lists in a tuple
    tried = tuple(list() for _ in range(length))
    while True:
        print('Known letters (shown in green)')
        for i in range(length):
            if known[i] == '':
                known[i] = get_char(f'Letter {i+1}: ', True)
                if known[i]:
                    positions_to_check.remove(i)
                    if known[i] in contained:
                        contained.remove(known[i])

        add_input_to_set(contained, "Contained (shown in yellow): ")
        positional_check(contained, tried, length)
        add_input_to_set(not_contained, "Not contained (shown in black): ")
        clear_screen()
        possibilitiesAUX = list()
        for word in possibilities:
            if not check_known(word, known):
                continue
            if not check_not_contained(word, not_contained, contained, positions_to_check):
                continue
            if not check_contained(word, contained, positions_to_check, tried):
                continue
            possibilitiesAUX.append(word)
        possibilities = possibilitiesAUX  # the list of possible words is updated
        print('------------------------------------')
        print('Possible words:')
        print(possibilities)  # shows the remaining words
        print('Letters: ', end='')  # prints the known word format
        for known_letter in known:
            if known_letter:
                print(known_letter, end='')
            else:  # the unknown letters are substituted by an underscore
                print('_', end='')
        print()
        print('Contained: ', ', '.join(char for char in contained))
        print('Tried: ')
        for i, tried_list in enumerate(tried):
            print(f' {i+1}: ', tried_list)
        print('Not contained:', ', '.join(char for char in not_contained))
        print('------------------------------------')
        restart = continue_check()
        if restart:
            break


if __name__ == '__main__':
    while True:
        guess()

from os import name, system


def create_word_list(length: int):
    """Imports all English words (https://github.com/dwyl/english-words)"""
    with open('EnglishWords.txt') as wordsFile:
        allWords = set(wordsFile.read().split())
        validWords = {word for word in allWords if len(word) == length}

    # The official Wordle game has some words that are not on the main list.
    # The Wordle word list is taken from the source code of the game, which is publicly available
    if length == 5:  
        with open('WordleWords.txt') as wordsFile:
            wordleWords = set(wordsFile.read().split())  # makes another set
            validWords.update(wordleWords)  # we update the main set

    # The final set is returned, ordered alphabetically
    return sorted(validWords)


def get_int(message: str, maximum: int):
    while True:
        print(message, end='')
        raw = input()
        if raw.isnumeric() == False:
            print('Invalid input')
            continue
        raw = int(raw)
        if raw <= maximum or maximum == 0:
            return raw


def get_char(message: str, single: bool):
    while True:
        print(message, end='')
        raw = input()
        if raw == '':
            return raw
        if raw.isalpha():
            raw = raw.lower()
            if single == False:
                return raw
            if len(raw) < 2:
                return raw
        print('Invalid input')


def positional_check(set_to_check: set, positions_list: list, length: int):
    for element in set_to_check:
        position = get_int(
            f'What position did you check "{element}" on? ', length)
        positions_list[position-1].append(element)


def add_input_to_set(main_set: set, message: str = ''):
    string = get_char(message, False)
    aux_set = set()
    for character in string:
        aux_set.add(character)
    main_set.update(aux_set)


def continue_check(msg: str):
    """Requires a positive or negative input and return it as a bool"""
    while True:
        check = input(f"{msg}? [Yes/ No] ")
        if check in ('Yes', 'Y', 'yes', 'y', '1'):
            return True
        if check in ('No', 'N', 'no', 'n', '0'):
            return False


def clear_screen():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')


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
    """Checks if the word contains any letter that should not be contained."""
    is_contained = True
    for character in contained:
        is_contained = False
        for i in positions_to_check:
            if character == word[i] and character not in tried[i]:
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
    # Letters tried for every position, as lists in a tuple
    tried = tuple(list() for _ in range(length))
    while True:
        print('Known letters (shown in green)')
        for i in range(length):
            if known[i]:
                continue
            known[i] = get_char(f'Letter {i+1}: ', True)
            if known[i] == '':
                continue
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
        if continue_check('End round'):
            break


if __name__ == '__main__':
    while True:
        guess()
        if not continue_check('Start new round'):
            break

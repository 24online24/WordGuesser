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


def positional_check(set_to_check, positions_list):
    for element in set_to_check:
        position = int(input(f"What position did you check {element} on? "))
        positions_list[position-1].append(element)


def add_input_to_set(main_set, message=''):
    string = input(message)
    aux_set = set()
    for character in string:
        aux_set.add(character)
    main_set.update(aux_set)


# depending on the specific game, words can have various lengths
length = int(input('Word length: '))
# a list of all words is initially created
possibilities = create_word_list(length)

letter = list()  # the array of known letters
for i in range(length):
    letter.append('')

contained = set()  # letters known to be in the word, but not the position
not_contained = set()  # letters known to not be in the word
# letters tried for every position, as lists in a tuple
tried = tuple(([] for i in range(length)))

while True:  # this will work for any number of rounds
    print('Known letters (shown in green)')
    for i in range(length):  # checks for new letters
        if letter[i] == '':  # if a letter is known, its position is ignored for later checks
            print('Letter {}: '.format(i+True), end='')
            letter[i] = input()
            if letter[i] in contained:
                contained.remove(letter[i])

    add_input_to_set(contained, "Contained (shown in yellow): ")
    positional_check(contained, tried)
    add_input_to_set(not_contained, "Not contained (shown in black): ")

    possibilitiesAUX = list()
    for word in possibilities:  # checks every word from the current possibilities

        ok_known = True  # the word supposedly matches all known letters
        for i in range(length):  # checks for every letter
            if letter[i]:  # if that position has a known letter
                if word[i] != letter[i]:  # checks if the word matches
                    ok_known = False  # if one letter doesn't match, the word is not valid

        ok_contained = True  # checks if all contained letters appear in word
        for character in contained:  # every letter that is contained must be checked
            ok_contained = False  # supposes a letter does not appear
            for i in range(length):  # checks for every letter position
                if letter[i] == '':  # ignores positions with known letters in them
                    if character == word[i]:  # if the letter appears
                        # and if it has not been tried in this position already
                        if character not in tried[i]:
                            ok_contained = True  # the boolean variable is switched
                        break  # it doesn't check for said letter anymore
            if ok_contained == False:  # it a letter didn't appear
                break  # it doesn't check for other letters

        # supposes the word is valid and doesn't containe any character it shouldn't
        ok_not_contained = True
        for character in not_contained:  # ever letter that we know is not contained must not be present
            if character not in contained:
                for i in range(length):  # checks for every letter position
                    if letter[i] == '':  # ignores positions with known letters in them
                        if character == word[i]:  # if one letter is present,
                            ok_not_contained = False  # the word is not valid

        if ok_known and ok_contained and ok_not_contained:  # if yes, it is added for the next round of checking
            possibilitiesAUX.append(word)

    possibilities = possibilitiesAUX  # the list of possible words is updated
    print('------------------------------------')
    print('Possible words:')
    print(possibilities)  # shows the remaining words
    print('Letters: ', end='')  # prints the known word format
    for i in range(length):
        if letter[i]:
            print(letter[i], end='')
        else:  # the unknown letters are substituted by an underscore
            print('_', end='')
    print()
    print('Contained:', ', '.join(character for character in contained))
    print('Tried: ')
    for i in range(length):
        print(f' {i+1}: ', end='')
        print(tried[i])

    print('Not contained:', ', '.join(character for character in not_contained))
    print('------------------------------------')

# TO DO
#   
#   
# Done
#   - remove letter from contained if found position
#   - optimize letter indexing so that known letters are not checked anymore
#   - contianed and not_contained made into sets from strings
#   - add known tried positions for contained letters
#   - positional check prompts for every contained letter,
#   not just the ones added on the last step
#   - show colors in messages
#   - Display tried tuple nicer 
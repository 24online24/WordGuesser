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


def add_input_to_set(main_set, message=''):
    string = input(message)
    for character in string:
        main_set.add(character)


# depending on the specific game, words can have various lengths
length = int(input('Word length: '))
# a list of all words is initially created
possibilities = create_word_list(length)

letter = []  # the array of known letters
for i in range(length):
    letter.append('')

contained = set()  # letters known to be in the word, but not the position
not_contained = set()  # letters known to not be in the word

while True:  # this will work for any number of rounds

    for i in range(length):  # checks for new letters
        if letter[i] == '':  # if a letter is known, its position is ignored for later checks
            print('Letter {}: '.format(i+1), end='')
            letter[i] = input()
            if letter[i] in contained:
                contained.remove(letter[i])

    add_input_to_set(contained, "Contained: ")
    add_input_to_set(not_contained, "Not contained: ")

    possibilitiesAUX = []
    for word in possibilities:  # checks every word from the current possibilities
        ok_known = 1  # the word supposedly matches all known letters
        for i in range(length):  # checks for every letter
            if letter[i]:  # if that position has a known letter
                if word[i] != letter[i]:  # checks if the word matches
                    ok_known = 0  # if one letter doesn't match, the word is not valid

        count_contained = 0
        for character in contained:  # every letter that is contained must be checked
            for i in range(length):  # checks for every letter position
                if letter[i] == '':  # ignores positions with known letters in them
                    if character == word[i]:
                        count_contained += 1
                        break
        ok_contained = (count_contained == len(contained))

        ok_not_contained = 1
        for character in not_contained:  # ever letter that we know is not contained must not be present
            for i in range(length):  # checks for every letter position
                if letter[i] == '':  # ignores positions with known letters in them
                    if character == word[i]:
                        ok_not_contained = 0  # if one letter is present, the word is not valid
            
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
    print('Not contained:', ', '.join(character for character in not_contained))
    print('------------------------------------')

# TO DO
#   - add known invalid positions for contained letters
# Done
#   - remove letter from contained if found position
#   - optimize letter indexing so that known letters are not checked anymore
#   - contianed and not_contained made into sets from strings
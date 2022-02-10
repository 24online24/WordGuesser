def createWordList(length):
    # takes all English words (https://github.com/dwyl/english-words)
    with open('EnglishWords.txt') as wordsFile:
        # a set is made, so that no words appear twice
        allWords = set(wordsFile.read().split())
        # filters all the words with a specific length
        validWords = {word for word in allWords if len(word) == length}

    if length == 5:  # The official Wordle game has some words that are not on the main list
        # the Wordle word list is taken from the source code of the game, which is publicly available
        with open('WordleWords.txt') as wordsFile:
            wordleWords = set(wordsFile.read().split()) # makes another set 
            validWords.update(wordleWords) # we update the main set

    return sorted(validWords) # the final set is returned, ordered alphabetically


# depending on the specific game, words can have various lengths
length = int(input('Word length: '))
# a list of all words is initially created
posibilities = createWordList(length)


while True:  # this will work for any number of rounds
    letter = []  # the array of known letters
    for i in range(length):
        print('Letter {}: '.format(i+1), end='')
        letter.append(input())
    contained = input("Contained: ")  # the letters known,
    notContained = input("Not contained: ")

    posibilitiesAUX = []
    for word in posibilities:  # checks every word from the current possibilities
        ok = 1  # the word is supposedly valid
        for i in range(length):    # checks for every letter
            if letter[i]:     # if that position has a known letter
                if word[i] != letter[i]:  # checks if the word matches
                    ok = 0  # if one letter doesn't match, the word is not valid
        for character in contained:  # every other letter that is contained must be checked
            if character not in word:
                ok = 0  # if one letter is not present, the word is not valid
        for character in notContained:  # ever letter that we know is not contained must not be present
            if character in word:
                ok = 0  # if one letter is present, the word is not valid
        if ok:  # if yes, it is added for the next round of checking
            posibilitiesAUX.append(word)

    posibilities = posibilitiesAUX # the list of possible words is updated
    print(posibilities) # shows the remaining words

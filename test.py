contained = set()
letter = ['a', '1']
i = 0
print(type(contained))
contained.add('a')
if letter[i] in contained:
    contained = contained.remove(letter[i])
print(type(contained))
contained.add(5)
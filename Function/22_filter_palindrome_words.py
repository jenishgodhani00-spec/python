words = ['madam', 'python', 'racecar', 'hello', 'level', 'world', 'radar']
palindromes = list(filter(lambda word: word == word[::-1], words))
print(palindromes)

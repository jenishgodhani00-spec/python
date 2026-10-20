numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
even = filter(lambda number: number % 2 == 0, numbers)
result = list(map(lambda number: number * number, even))
print(result)

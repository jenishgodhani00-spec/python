nums = [2, 3, 4, 5, 6]
primes = [x for x in nums if all(x % i != 0 for i in range(2, int(x**0.5)+1)) and x > 1]
print('Primes:', primes)
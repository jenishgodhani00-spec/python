def is_prime(x):
    return x > 1 and all(x % i != 0 for i in range(2, int(x**0.5)+1))
print(is_prime(7))
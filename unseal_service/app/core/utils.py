import random
import base64
from functools import reduce

PRIME = 2**521 - 1

def split_secret(secret, total_shares, threshold):
    if threshold > total_shares:
        raise ValueError("Threshold cannot be greater than total shares")

    secret_int = int.from_bytes(secret.encode(), "big")
    coeffs = [secret_int] + [random.SystemRandom().randint(1, 2**256) for _ in range(threshold - 1)]

    def eval_poly(x):
        return sum([coeff * (x ** i) for i, coeff in enumerate(coeffs)])

    shares = []
    for i in range(1, total_shares + 1):
        x = i
        y = eval_poly(x)
        shares.append((x, y))

    encoded = [f"{x}-{base64.b64encode(y.to_bytes(64, 'big')).decode()}" for x, y in shares]
    return encoded

def recover_secret(shares):
    def lagrange_interpolate(x, x_s, y_s):
        def _l(i):
            xi, yi = x_s[i], y_s[i]
            terms = [(x - x_s[m]) * pow(xi - x_s[m], -1, PRIME) for m in range(len(x_s)) if m != i]
            return reduce(lambda a, b: a * b % PRIME, terms, 1) * yi

        return sum(_l(i) for i in range(len(x_s))) % PRIME

    x_s, y_s = [], []
    for share in shares:
        x, y_b64 = share.split('-')
        x = int(x)
        y = int.from_bytes(base64.b64decode(y_b64), 'big')
        x_s.append(x)
        y_s.append(y)

    secret_int = lagrange_interpolate(0, x_s, y_s)
    secret_bytes = secret_int.to_bytes((secret_int.bit_length() + 7) // 8, "big")
    return secret_bytes.decode()
def round_hundreds(n):
    try:
        n = (n / 100) // 1
        return n
    except TypeError:
        pass

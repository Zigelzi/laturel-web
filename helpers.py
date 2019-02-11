def calc_drivepowertax(n):
    try:
        n = (n / 100) // 1
        n = n * 0.055
        return n
    except TypeError:
        pass

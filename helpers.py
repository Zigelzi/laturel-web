def round_hundreds(n):
    try:
        n = (n / 100) // 1
        return n
    except TypeError:
        pass

    '''
    Calculating car deprecation 
    '''
def deprecation(purchase, rate, years):
    try:
        depr_value = 0
        depr = purchase * (1 - rate/100) ** years
        depr_value = purchase - depr
    except:
        pass
    return depr_value

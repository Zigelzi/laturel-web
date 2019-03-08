def round_hundreds(n):
    try:
        n = (n / 100) // 1
        return n
    except TypeError:
        pass


#  Calculating car deprecation
def deprecation(purchase, rate, years):
    try:
        depr_value = 0
        depr = purchase * (1 - rate/100) ** years
        depr_value = purchase - depr
    except:
        pass
    return depr_value

# Calculates car value, yearly deprecation, total deprecation and yearly costs.
def depr_oper(purchase, rate, years, cost):
    try:
        car_value = []
        depr_value = []
        depr_yearly = []
        ycost = []
        for y in range(1, years+1):
            car_value.append(purchase * (1 - rate/100) ** y)
            depr_value.append(int(purchase - car_value[y-1]))
            if y == 1:
                depr_yearly.append(int(purchase - car_value[y-1]))
            else:
                depr_yearly.append(int(car_value[y-2] - car_value[y - 1]))
        for y in range(1, years+1):
            ycost.append(int(cost * y))
    except:
        pass
    return depr_value, depr_yearly, ycost
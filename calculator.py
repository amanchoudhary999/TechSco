def fac(x):
    prod = 1
    for i in range(1, x+1):
        prod *= i
    return prod


def sine(x):
    val = 0
    term = 50
    for i in range(0, term):
        if i%2 == 0:
            n = (2 * i) + 1
            val += (x ** n)/fac(n)
        else:
            n = (2 * i) + 1
            val -= (x ** n) / fac(n)
    return val


def cos(x):
    val = 1
    term = 51
    for i in range(1, term):
        if i % 2 == 1:
            n = (2 * i)
            val -= (x ** n) / fac(n)
        else:
            n = (2 * i)
            val += (x ** n) / fac(n)
    return val


def tan(x):
    val = x + (x**3 / 3) + (2 * x**5 /15) + (17 * x**7 / 315) + (62* x**9 / 2835)
    return val


print("______SCIENTIFIC__CALCULATOR______")
result = float(input("Enter first number"))
while True:
    print("____OPERATIONS____")
    print("1 - ADDITION\n 2-SUBSTRACTION\n3-MULTIPLICATION\n4-DIVISION\n5-EXPONENT\n6-COSINE\n7-SINE\n8-TANGENT\n9-FACTORIAL\n0-EXIT")
    opr = int(input("Enter opperation number"))
    if opr in [1,2,3,4,5]:
        num =  float(input("Enter second number(exp )"))
        if opr == 1:
            result += num
        elif opr == 2:
            result -= num
        elif opr == 3:
            result *= num
        elif opr == 4:
            result /= num
        else :
            result **= num
    elif opr in [6,7,8,9]:
        if opr == 6:
            result = cos(result)
        elif opr == 7:
            result = sine(result)
        elif opr == 8:
            result = tan(result)
        else:
            result = fac(result)
    print("value is ",result)
    if opr not in [1,2,3,4,5,6,7,8,9]:
        print("final answer is ",result)
        break
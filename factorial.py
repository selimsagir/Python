def factorial(x):
    if x == 1:
        return 1
    else:
        return (x*factorial(x-1))


num = 10

print("the factorial of ", num, "is" , factorial(num))

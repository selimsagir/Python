# if statement

# x = int(input("Please enter an integer"))
# if x < 0:
#     x = 0
#     print('Negative changed to zero')
# elif x == 0:
#     print('Zero')
# elif x == 1:
#     print('Single')
# else:
#     print('More')

# words = ['cat', 'window','defenestrate']
# for w in words:
#     print(w, len(w))

# # Create a sample collection
# users = {'Selim': 'active','Semanur':'inactive', 'Ben':'active'}

# # Strategy:  Iterate over a copy
# for user, status in users.copy().items():
#     if status == 'inactive':
#         del users[user]
# # Strategy:  Create a new collection
# active_users = {}
# for user, status in users.items():
#     if status == 'active':
#         active_users[user] = status

# for i in range(5):
#     print(i)

# list(range(-10, -100, -30))


# a = ['Selim', 'bir','kaleme', 'sahip']
# for i in range(len(a)):
#     print(i,a[i])



# sum(range(5))


# # find prime numbers
# for n in range(2,10):
#     for x in range(2,n):
#         if n % x == 0:
#             print(n,'equals', x, '*', n/x)
#     else:
#         #loop fell through without finding a factor
#         print(n, 'is a prime number')


# for num in range(2,10):
#     if num % 2 == 0:
#         print("found an even number", num)
#         continue
#     print("Found a odd number", num)



# def http_error(status):
#     match status:
#         case 400:
#             return "bad request"
#         case 404:
#             return "not found"
#         case 418:
#             return  "cay bardagı"
#         case _:
#             return "buda neydi"

# class Point:
#     x: int
#     y: int

# def where_is(point):
#     match point:
#         case Point(x=0, y=0):
#             print("Origin")
#         case Point(x=0, y=y):
#             print(f"Y={y}")
#         case Point(x=x, y=0):
#             print(f"X={x}")
#         case Point():
#             print("Somewhere else")
#         case _:
#             print("Not a point")


# Point(1, var)
# Point(1, y=var)
# Point(x=1, y=var)
# Point(y=var, x=1)

# from enum import Enum
# class Color(Enum):
#     RED = 'red'
#     GREEN = 'green'
#     BLUE = 'blue'

# color = Color(input("Enter your choice of 'red', 'blue' or 'green': "))

# match color:
#     case Color.RED:
#         print("I see red!")
#     case Color.GREEN:
#         print("Grass is green")
#     case Color.BLUE:
#         print("I'm feeling the blues :(")




# def scope_test():
#     def do_local():
#         spam = "local spam"
#     def do_nonlocal():
#         nonlocal spam
#         spam = "non localspam"
#     def do_global():
#         global spam
#         spam = "global spam"

#     spam = "test spam"
#     do_local()
#     print("After local assignment:", spam)
#     do_nonlocal()
#     print("After nonlocal assignment:", spam)
#     do_global()
#     print("After global assignment:", spam)

# scope_test()
# print("In global scope:", spam)



class Complex:
    def __init__(self, realpart, imagpart):
        self.r = realpart
        self.i = imagpart

x = Complex(3.0,20.0)
print(x.r,x.i)
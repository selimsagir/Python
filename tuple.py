import this


thistuple = ("apple", "banana","cherry")
print(len(thistuple))

thistuple = ("apple", "banana", "cherry", "orange", "kiwi", "melon", "mango")
print(thistuple[2:5])

thistuple = ("apple", "banana", "cherry", "orange", "kiwi", "melon", "mango")
print(thistuple[2:])
thistuple = ("apple", "banana", "cherry", "orange", "kiwi", "melon", "mango")
print(thistuple[-4:-1])

#convert tuple to list
x = ("apple", "banana", "cherry")
y = list(x)
y[1] ="kiwi"
x = tuple(y)
print(x)

thistuple = ("apple", "banana", "cherry", "orange", "kiwi", "melon", "mango")
for i in range(len(thistuple)):
    print(thistuple[i])
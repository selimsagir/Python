# sum = 1+2+3+..+n


n = 10

sum =0
i = 1

while i <= n:
    sum = sum + i
    i = i + 1

print("The sum is " , sum)

counter = 0

while counter < 3:
    print("inside loop")
    counter = counter + 1
else:
    print("outside of the loop")

for val in "string":
    if val == "i":
        break
    print(val)

print("The End")

for val in "string":
    if val == "i":
        continue
    print(val)
print("the end")

def greet(name):
    print("hi " + name + " how are you")
greet("selim")


def greetName(name, msg="Good morning"):
    print("Hi " + name + msg )

greetName("selim")
greetName("selim", "how are you?")    

def printName(*names):
    for name in names:
        print("hello", name  )

printName("selim", "selim 2","selim 3")
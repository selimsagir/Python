

c = 0

def add():
    global c
    c = c + 1
    print("inside func:", c)

add()
print("outside func:",c)
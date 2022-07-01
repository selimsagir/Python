from re import X


def foo():
    x= 10

    def bar():
        global x 
        x = 20

    print("Before calling bar:" , x)
    print("calling bar now")
    bar()
    print("After called bar:", x)

foo()
print("Global x: ", x)
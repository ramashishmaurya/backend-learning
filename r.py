def function(func):

    def dealwithperson(fuck):
        def wrapper():
            print("hellp=o ji ")
            func()
            print("bye ji")
            fuck()
        return wrapper
    return dealwithperson


def func():
    print("this is func function right")

@function(func)
def fuck():
    print('function of fuck')

fuck()


def arguments(*args):
    print(args)

arguments(12,12,4)


from time import sleep

def some_heavy_method(a,b):
    # emulate as if the method run in 10 seconds
    sleep(10)
    return a+b

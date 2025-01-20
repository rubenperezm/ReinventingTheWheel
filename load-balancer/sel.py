import random

# For static selection methods, we could pass the number of backends as an argument 
# to the function. However, if we want to implement dynamic selection methods,
# we need to pass the list of backends. Therefore, we will pass the list of backends.

def rr(hosts):
    i = 0
    while True:
        yield i
        i = (i + 1) % len(hosts)

def rand(hosts):
    while True:
        yield random.choice(len(hosts))

def backend_selection(hosts, available_backends, method):
    count = 0
    generator = method(hosts)
    while True:
        i = next(generator)

        if available_backends[i]:
            count = 0
            yield hosts[i]

        else:
            count += 1
            if count == len(hosts):
                raise Exception("No healthy backends available")
        
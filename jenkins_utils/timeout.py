from functools import wraps
import time

def timeout(timeout):
    def timeout_decorator(func):
        @wraps(func)
        def func_wrapper():
            for _ in range(0,timeout):
                ret = func()
                if ret:
                    return ret
                else:
                    print "Not returned.."
                    time.sleep(1)
            raise Exception("Quit after {} secs".format(timeout))
        return func_wrapper
    return timeout_decorator


def otherfunc():
    pass

@timeout(3)
def myfunc():
    if otherfunc():
        print "Got True"
        return True

myfunc()
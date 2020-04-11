###########
# Imports #
###########
from threading import Thread

#################
# Main Function #
#################
def toThread(func):
    @wraps(func)
    def asyncWrapper(*args,**kwargs):
        t=Thread(target=func,args=args,kwargs=kwargs)
        t.start()
    return async_wrapper

from threading import Thread

def async(func):
    def async_wrapper(*args,**kwargs)
        t=Thread(target=func,args=args,kwargs=kwargs)
        t.start()
    return async_wrapper

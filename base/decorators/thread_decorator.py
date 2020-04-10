from threading import Thread
from functools import wraps

def async(func):
	# polecam uzywac "@wraps", poniewaz wtedy nazwa funkcji 
	# i inne jej atrybuty pozostana bez zmian
	@wraps(func)
    def async_wrapper(*args,**kwargs)
        t=Thread(target=func,args=args,kwargs=kwargs)
        t.start()
    return async_wrapper

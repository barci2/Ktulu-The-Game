from threading import Thread
from functools import wraps

def action(func):
	# polecam uzywac "@wraps", poniewaz wtedy nazwa funkcji 
	# i inne jej atrybuty pozostana bez zmian
	@wraps(func)
    def action_wrapper(self,*args,**kwargs):
        self.

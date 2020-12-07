
DEBUG = False

def prints(*args, **kwargs):
   if DEBUG:
      print(*args, flush=True,**kwargs)
import os
import multiprocessing
_home = os.environ['PWD']

#workers = multiprocessing.cpu_count() * 2
workers = 64
max_requests = 1000
loglevel = 'debug'
accesslog = os.path.join(_home, "paddles.access.log")
errorlog = os.path.join(_home, "paddles.error.log")

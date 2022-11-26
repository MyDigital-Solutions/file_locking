`singleinstance.py`  
A template for a Python script with single-instance check using exclusive locking on a lockfile.

`runner.py`  
A script to run a command in an endless loop with a minimum interval between iterations, specified in seconds.  
For example: `runner.py 60 ./singleinstance.py [args...]`  
would run `./singleinstance.py` and when its process ends it would run it again. In case the process ends sooner than 60s, the script waits for the rest of the time first.

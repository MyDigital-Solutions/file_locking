import sys, os, time

# template for a script that should ensure that only one instance gets running
# via POSIX lock on a lockfile

# define a lockfile path for the script
LOCKFILE="/tmp/singleinstance.py.lock"
# can define a custom exit status for the case when another holds the lock
RETURNCODE_ANOTHERINSTANCE=99


def main():
    # main program
    print("-- sleep start")
    time.sleep(60)
    print("-- sleep end")


def script():
    if os.name == "nt":
        raise NotImplementedError("Windows is not supported")

    import fcntl, errno
    with open(f"{LOCKFILE}", 'w+') as lockfile:
        # acquire exclusive lock on lockfile or fail immediately (LOCK_NB)
        try:
            fcntl.lockf(lockfile, fcntl.LOCK_EX | fcntl.LOCK_NB) # acquire lock
            lockfile.write(f"{os.getpid()} {time.time()}") # can write some info into the lockfile (pidfile)
            lockfile.flush()
            # call entry point function for the main program here
            ret = main()
            # have to hold lock until exit
            sys.exit(ret)
        except OSError as e:
            # OSError raised and errno is set if another process already holds the lock
            # on linux, mac == EWOULDBLOCK with LOCK_NB
            if e.errno in [errno.EWOULDBLOCK]:
                print(f"{__file__}: another instance is running", file=sys.stderr)
                sys.exit(RETURNCODE_ANOTHERINSTANCE)


if __name__ == '__main__':
    script()

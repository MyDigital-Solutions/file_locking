#!/usr/bin/env python3

# A script to run a command in an endless loop with a minimum interval between iterations, specified in seconds
# Usage: runner.py <interval> <command> [args...]


import logging

logger = logging.getLogger(__name__)
log = logger.info


import sys, os, time
import argparse


def main(interval, cmd, cmd_args):
    while True:
        log(f"run (min. interval {interval}s): {cmd}")
        time_start = time.time()

        ret = os.spawnlp(os.P_WAIT, cmd, cmd, *cmd_args)

        time_end = time.time()
        dur_process = time_end - time_start

        str_warn_status = f"with status: {ret} " if ret != 0 else ""
        log(f"process ended {str_warn_status}(duration: {dur_process}s): {cmd}")

        # if the duration was less the min. interval, wait for the rest of the time
        if dur_process < interval:
            dur_sleep = interval - dur_process
            time.sleep(dur_sleep)


def script():
    # logformat = "%(levelname)s:%(module)s:%(funcName)s: %(message)s"
    logformat = "%(levelname)s:%(filename)s: %(message)s"
    logging.basicConfig(level=logging.INFO, format=logformat)

    p = argparse.ArgumentParser()
    p.add_argument("interval", type=int, metavar="interval")
    p.add_argument("command")
    p.add_argument('args', nargs=argparse.REMAINDER)
    args = p.parse_args()

    interval = args.interval
    if not interval > 0: raise ValueError()
    cmd = args.command
    cmd_args = args.args

    main(interval, cmd, cmd_args)


if __name__ == '__main__':
    script()

#!/usr/bin/env python

# Sometimes the Django development server doesn't release its port when
# killed.  This program will find the process and kill -15 it.  If that doesn't
# work, it will be kill -9'd.

from subprocess import Popen, PIPE


def pid_status(pid):
    """Check if process ID is running and return boolean for status."""
    GREP_PID = 'ps aux | grep {process} | grep -v grep'
    cmd = Popen(GREP_PID.format(process=pid), stdout=PIPE, shell=True)
    out, err = cmd.communicate()
    processes = out.split('\n')
    if processes == ['']:
        print 'Process {} killed.'.format(pid)
        return False
    else:
        print 'Process {} still running.'.format(pid)
        return True


def kill_pid(pid, level=15):
    """Kill specified process.  Default to level 15, e.g. kill -15 PID."""
    KILL_CMD = 'kill -{level} {process}'
    print 'Killing process {}...'.format(pid)
    cmd = Popen(KILL_CMD.format(level=level, process=pid), stdout=PIPE,
                shell=True)
    out, err = cmd.communicate()


def find_pids(processes):
    """Return generator object of process IDs."""
    for process in processes:
        process = process.split(' ')
        row = [p for p in process if p != '']
        try:
            yield row[1]
        except IndexError:
            continue


def get_processes():
    """Run process command and return output."""
    GREP_FIND = 'ps aux | grep python | grep runserver | grep -v grep'
    cmd = Popen(GREP_FIND, stdout=PIPE, shell=True)
    out, err = cmd.communicate()
    processes = out.split('\n')

    if processes == ['']:
        print 'No Django development servers found.'
        return
    else:
        print 'Django development server processes:'
        print '===================================='
        print out
        return processes


def main():
    """Kick off tasks to find and kill Django development servers."""
    processes = get_processes()

    if not processes:
        return

    pids = find_pids(processes)
    for pid in pids:
        kill_pid(pid)
        status = pid_status(pid)
        if status:
            kill_pid(pid, 9)


if __name__ == '__main__':
    main()

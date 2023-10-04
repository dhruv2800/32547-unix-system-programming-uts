"""
A program for reading log file containing 
unix process information and printing the
process information in a tabular format.
"""

import sys
import os
import re
import argparse

def define_flags():
    """Define the command line flags."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--all', help='Print all lines of the logfile', action='store_true')
    parser.add_argument('-m', '--memory', help='Print total memory used by all processes', action='store_true')
    parser.add_argument('-t', '--total', help='Print total cpu time', action='store_true')
    parser.add_argument('-s', '--threshhold', help='Memory threshold', action='store')
    parser.add_argument(dest='logfile', help='Logfile to read', action='store', metavar='logfile')
    return parser.parse_args()

def read_logfile(logfile):
    """Read the logfile and return a list of lines."""
    try :
        with open(logfile, 'r') as f:
            return f.readlines()
    except IOError:
        print ('Unable to read logfile')
        sys.exit(1)


def parse_line(line):
    """Parse a line and return a dictionary of the process information."""
    line = line.strip()
    line = re.sub(r'\s+', ' ', line)
    line = line.split(' ')
    return {'pid': line[0], 'mem': line[1], 'cpu_time': line[2], 'program_name': line[3]}

def parse_logfile(logfile):
    """Parse the logfile and return a list of dictionaries."""
    lines = read_logfile(logfile)
    return [parse_line(line) for line in lines]

def sort_by_program_name(processes):
    """Sort processes by program name."""
    return sorted(processes, key=lambda k: k['program_name'])

def get_total_memory(processes):
    """Return the total memory used by all processes."""
    return sum([int(p['mem']) for p in processes])

def get_total_cpu_time(processes):
    """Return the total cpu time used by all processes."""
    return sum([int(p['cpu_time']) for p in processes])

def filter_by_memory(processes, threshhold):
    """Return processes that use more than threshhold memory."""
    return [p for p in processes if int(p['mem']) >= int(threshhold)]

def main():
    """Main function."""
    flags = define_flags()
    processes = parse_logfile(flags.logfile)
    
    if flags.all:
        if len(processes) == 0:
            print ('No processes found')
            sys.exit(1)
        else:
            processes = sort_by_program_name(processes)
            for p in processes:
                print ('{pid} {mem} {cpu_time} {program_name}'.format(**p))
    
    if flags.memory:
        if len(processes) == 0:
            print ('No processes found')
            sys.exit(1)
        else:
            print ("Total memory size:",get_total_memory(processes),"KB")
    if flags.total:
        if len(processes) == 0:
            print ('No processes found')
            sys.exit(1)
        else:
            print ("Total CPU time:",get_total_cpu_time(processes),"seconds")
    if flags.threshhold:
        matches = filter_by_memory(processes, flags.threshhold)
        if len(matches) == 0:
            print ('No processes found withe specified memory size')
            sys.exit(1) 
        else:
            for p in matches:
                print ('{pid} {mem} {cpu_time} {program_name}'.format(**p))

if __name__ == '__main__':
    main()





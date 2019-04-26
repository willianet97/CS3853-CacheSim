#!/usr/bin/python

import argparse
import sys
import math
import logging
import yaml
import gzip

######## constants ##############
cache_line_size = 64
offset_bits = int(math.log(64, 2))
######## user interface #########
def main():

    parser = argparse.ArgumentParser(description='Cache Simulator.')
    parser.add_argument('-s', '--size', metavar='N', type=str, dest='size',
                        help='the size of the cache in B, KB or MB', required=True)
    parser.add_argument('-a', '--assoc', dest='assoc', type=int, metavar='s',
                        help='the set associativity of the cache', required=True)
    parser.add_argument('-f', '--file', metavar='FILENAME', type=str, dest='file',
                        help="name of the input memory trace file; if the file is "
                        "in gzip format, the file name must end with .gz",
                        required=True)
    parser.add_argument('--debug', dest='debug', action='store_const',
                        const=True, default=False,
                        help='enable debugging logs')
    parser.add_argument('--print', dest='enable_print', action='store_const',
                        const=True, default=False,
                        help='enable cache content output')
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    
    cacheSize = parse_size(args.size)

    memory = Memory()
    cache = Cache()

    trace_file = open(arguments['trace_file'])
    trace = trace_file.read().splitlines()
    trace = [item for item in trace if not item.startswith('#')]

    simulate(trace)

######## helper functions ########

# parse the user-input size string, returns the size in bytes

def parse_size(size):
    try:
        if size.endswith('KB'): 
            s = int(size[:-2]) * 1024
        elif size.endswith('MB'):
            s = int(size[:-2]) * 1024 * 1024
        elif size.endswith('B'):
            s = int(size[:-1])
        else: # just the integer
            s = int(size);
    except ValueError:
        print("Invalid cache size")
        sys.exit(1)
    return s

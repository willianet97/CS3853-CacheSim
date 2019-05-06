#!/usr/bin/python

import argparse
import sys
import math
import logging
import gzip
import cache

######## constants ##############
cache_line_size = 64
offset_bits = int(math.log(64, 2))

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

####### simulator #############

def simulate(cache, trace):
    global misses
    global hits
    for line in trace:
        splitLine = line.split()
        if (len(splitLine) == 3):
            trash, op, address = splitLine
            if op == 'R':
                result = cache.read(address)
                if(result == 0):
                    misses += 1
                    cache.load(address)
                    cache.read(address)
                else:
                    hits += 1

            else:
                result = cache.write(address)
                if(result == 0):
                    misses += 1
                    cache.load(address)
                    cache.write(address)
                else:
                    hits += 1
    print_results(misses, hits)
    

def print_results(misses, hits):
    ratio = (hits / ((hits + misses) if misses else 1)) * 100
    print("Hit/Miss Ratio: {0:.2f}%".format(ratio) + "\n")


######## user interface #########
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
associativity = 2 ** args.assoc

cache = cache.Cache(cacheSize, cache_line_size, associativity, offset_bits)

trace_file = open(args.file)
trace = trace_file.read().splitlines()
trace = [item for item in trace if not item.startswith('#')]

hits = 0
misses = 0

simulate(cache, trace)


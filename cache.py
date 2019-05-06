import random
import math
from line import Line

class Cache:
    def __init__(self, cacheSize, cache_line_size, associativity, offset_bits):

        #Parameters configured by the queuer
        self.size = cacheSize
        self.associativity = associativity
        self.cache_line_size = cache_line_size
        self.number_sets = (cacheSize/(associativity * cache_line_size))
        self.indexSize = int(math.log(self.number_sets, 2))
        self.offset_bits = offset_bits

        #Initialize the data 
        self._lines = [Line(cache_line_size) for i in range(cacheSize//cache_line_size)]

    def read(self, address):
        block_offset, index, tag = self.parse_address(address)
        set_cache = self._get_set(address)
        line = None

        for candidate in set_cache:
            if candidate.tag == tag and candidate.valid:
                line = candidate
                break
        if line:
            result = 1
            self._update_queue(line, set_cache)
        else:
            result = 0

        return result

    def write(self, address):
        block_offset, index, tag = self.parse_address(address)
        set_cache = self._get_set(address)
        for candidate in set_cache:
            if candidate.tag == tag and candidate.valid:
                line = candidate
                break
        if line:
                result = 1
                line.modified = 1
        else: 
            result = 0
        self._update_use(line, set_cache)
        return result

    def load(self, address):
        """Load a block of memory into the cache.
        :param int address: memory address for data to load to cache
        :param list data: block of memory to load into cache
        :return: tuple containing victim address and data (None if no victim)
        """
        block_offset, index, tag = self.parse_address(address)
        cache_set = self._get_set(address)
        victim_info = None

        # Select the victim
        victim = cache_set[0]

        for index in range(len(cache_set)):
            if cache_set[index].queue < victim.queue:
                victim = cache_set[index]

        victim.queue = 0

        # Store victim info if modified
        if victim.modified:
            victim_info = (index, victim.data)

        # Replace victim
        victim.modified = 0
        victim.valid = 1
        victim.tag = tag

        return victim_info


    def parse_address(self, address):
        decimal = bin(int(address, 16))[2:]
        tag = decimal[0:len(decimal)-self.offset_bits-self.indexSize]
        if tag == '':
            tag = '0'
        index = decimal[len(decimal)-self.offset_bits-self.indexSize:len(decimal)-self.offset_bits]
        if index == '':
            index = '0'
        offset = decimal[len(decimal)-self.offset_bits:len(decimal)]
        return (offset, index, tag)

    def _update_queue(self, line, cache_set):
        """Update the queue bits of a cache line.
        :param line line: cache line to update queue bits 
        """

        queue = line.queue
        if line.queue < self.associativity:
            line.queue = self.associativity
            for other in cache_set:
                if other is not line and other.queue >= queue:
                    other.queue -= 1


    def _get_set(self, address):
        """Get a set of cache lines from a physical address.
        :param int address: memory address to get set from
        """
        decimal_address = bin(int(address, 16))[2:]
        set_mask = (self.size // (self.cache_line_size * self.associativity)) - 1
        set_num = (len(decimal_address) >> self.offset_bits) & set_mask
        index = set_num * self.associativity

        return self._lines[index:index + self.associativity]

        #print(index)
        #print(type(index))
        #return self._lines[index:index + self.associativity]

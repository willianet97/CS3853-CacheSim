def __init__(cacheSize, cache_line_size, associativity, offset_bits):

    #Parameters configured by the queuer
    self.associativity = associativity
    self.number_sets = (cacheSize/(associativity * cache_line_size))
    self.indexSize = int(math.log(number_sets, 2))
    self.offset_bits = offset_bits

    #Initialize the data 
    self._lines = [Line(cache_line_size) for i in range(cacheSize//cache_line_size)]

def read(self, address, misses, hits):
    block_offset, index, tag = self.parse_address(address)
    cache_set = self._get_set(index)
    line = None

    for candidate in set_cache:
        if candidate.tag == tag and candidate.valid:
            line = candidate
            break
    if line:
        hits = hits +1
        self._update_queue(line, cache_set)
    else:
        misses = misses +1

    return (misses, hits)
    

def write(self, address, misses, hits):
    block_offset, index, tag = self.parse_address(address)


def parse_address(address):
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


def _get_set(self, index):
        """Get a set of cache lines from a physical address.
        :param int address: memory address to get set from
        """
        return self._lines[index:index + self.associativity]

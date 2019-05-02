def __init__(word_size , block_size , cacheSize, cache_line_size, associativity, offset_bits):
        #Parameters configured by the user
        self.word_size = word_size
        self.block_size = block_size
        self.associativity = associativity
    
        self.number_sets = (cacheSize/(associativity * cache_line_size))
        
        #hash table that holds the cache data
        self.data = {}
        
        self.block_offset_size = offset_bits
        self.index_size = int(math.log(self.n_sets, 2))

        #Initialize the data 
        for i in range(self.n_sets):
            index = str(bin(i))[2:].zfill(self.index_size)
            if index == '':
                index = '0'
            self.data[index] = {}   #Create a dictionary of blocks for each set

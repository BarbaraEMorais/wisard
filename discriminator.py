from bitarray import bitarray


class Rams():

    def __init__(self,num_bits:None, bitarray_size:None, bitarray:None):
        self.num_bits = num_bits
        self.bitarray_size = bitarray_size
        self.bitarray = bitarray
        

#isso vai ficar no py de wisard q vou traduzit pra py
class Discriminator_t():

    def __init__(self,entry_size,tuple_size,num_rams=None,tuples_mapping=None,rams=None):
        self.entry_size = entry_size
        self.tuple_size = tuple_size
        self.num_rams = num_rams
        self.tuples_mapping = tuples_mapping
        self.rams = rams

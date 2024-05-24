"""
Status: REVISAR -> COM BITARRAY N PRECISO DEIXAR TUDO EM FUNÇÃO DO STRUCT DE C

Feito por Leandro Santiago em C
Convertido para py por Bárbara Morais

"""

import time
import random
from discriminator import Discriminator_t
from bitarray import bitarray
import numpy as np

def random_shuffle(array,n):
    random.seed(time.time())

    for i in range(n-1,0,-1):
        j = random.randint(0, i)
        temp = array[i].copy()
        array[i] = array[j].copy()
        array[j] = temp

def discriminator_new (entry_size,tuple_size):

    disc = Discriminator_t(entry_size,tuple_size)
    disc.num_rams = int(entry_size/tuple_size + ((entry_size%tuple_size) > 0)) #py pode transf em float
    #criando array bin setado com 0 em todos os elementos
    disc.tuples_mapping = bitarray(entry_size).setall(0)
     
    #gerando pseudo-random mapping

    for i in range(0, entry_size, 1):
        disc.tuples_mapping[i] = i

    random_shuffle(disc.tuples_mapping,entry_size)
    
    #print(entry_size)

    #for i in range(0, entry_size, 1):
    #   print(disc.tuples_mapping[i])

    #Alocando memória RAM
    disc.rams = bitarray(disc.num_rams).setall(0)

    #deslocamento à esquerda de bits no tamanho de tuple_size, mult 1 por 2^tuple_size
    num_bits = 1 << tuple_size
    #desloc à direita, divide num de bits por 2⁶
    bitarray_size = int(num_bits >> 6)

    bitarray_size += ((bitarray_size & 0x3F) > 0)

    for i in range(0, disc.num_rams, 1):
        disc.rams[i].num_bits = num_bits
        disc.rams[i].bitarray_size = bitarray_size
        ##prof me ajuda nessa aqui
        disc.rams[i].bitarray = np.uint64(disc.rams[i].bitarray_size).fill(0)
        #em c
        #disc->rams[i].bitarray = (uint64_t *)calloc(disc->rams[i].bitarray_size, sizeof(uint64_t));
    
    return disc

def discriminator_info(disc):

    print("Entry = ", disc.entry_size,"Tuples = ", disc.tuple_size, "RAMs = ", disc.num_rams)

    for i in range(0, disc.num_rams, 1):
        print("RAM ", i, disc.rams[i].num_bits, " bits\n")

        for j in range(0,disc.rams[i].bitarray_size,1):
            print(disc.rams[i].bitarray[j])

        print("\n")

def discriminator_train(disc, data):

    k = 0

    for i in range(0,disc.num_rams,1):
        addr_pos = disc.tuple_size -1
        addr = np.uint64(addr).fill(0)

        for j in range(0,disc.tuple_size,1):
            i1 = disc.tuples_mapping[k] >> 6 #Divide by 64 to find the bitarray id
            i2 = disc.tuples_mapping[k] & 0x3F #Obtain remainder to access the bitarray position

            #não entendi propósito desse
            addr |= (((data.bitarray[i1] & (1 << i2))>>i2) << addr_pos)
            addr_pos = addr_pos -1
            k = k+1

        i1 = addr >> 6 #Divide by 64 to find the bitarray id
        i2 = addr & 0x3F #Obtain remainder to access the bitarray position
        disc.rams[i].bitarray[i1] |= (1 << i2)

def discriminator_rank(disc, data):

    rank = 0
    k = 0 

    for i in range(0, disc.num_rams, 1):
        addr_pos = disc.tuple_size-1
        addr = np.uint64(addr).fill(0)

        for j in range(0,disc.tuple_size, 1):
            i1 = disc.tuples_mapping[k] >> 6 #Divide by 64 to find the bitarray id
            i2 = disc.tuples_mapping[k] & 0x3F #Obtain remainder to access the bitarray position

            #não entendi propósito desse
            addr |= (((data.bitarray[i1] & (1 << i2))>>i2) << addr_pos)
            addr_pos = addr_pos -1
            k = k+1

        i1 = addr >> 6 #Divide by 64 to find the bitarray id
        i2 = addr & 0x3F #Obtain remainder to access the bitarray position
        rank += (disc.rams[i].bitarray[i1] & (1 << i2)) >> i2

    return rank

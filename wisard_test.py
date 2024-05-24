"""

Status: concluído
Função: realizar o treinamento e rankeamento

"""

from bitarray import bitarray
from discriminator import Discriminator_t
from wisard import discriminator_rank, discriminator_train

entry_size = 100
num_tuples = 10

disc = Discriminator_t(entry_size,num_tuples)

#creating data 1
data = []
data1 = bitarray(542214)
data2 = bitarray(40000100)
data.append(data1)
data.append(data2)

#print(data)

discriminator_train(disc, data)

#data2

data_2 = []
data2_1 = bitarray(542210)
data2_2 = bitarray(400682236)
data_2.append(data2_1)
data_2.append(data2_2)

r = discriminator_rank(disc, data_2)

print("Rank = ", r)


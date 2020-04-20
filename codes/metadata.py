import os
import numpy as np
import matplotlib.pyplot

from copy import copy

def get_metadata(arq):
    count_instances = 0
    car = 0
    bus = 0
    mot = 0
    while(1):
        text = arq.readline()
        if text == '':
            break
        count_instances += 1
        if text.split(' ')[0] == '0':
            car += 1
        if text.split(' ')[0] == '1':
            bus += 1
        if text.split(' ')[0] == '2':
            mot += 1
    assert count_instances == int(car + bus + mot), "%r, %r, %r, %r" % (count_instances, car, bus, mot)

    return (count_instances, car, bus, mot)


PATH = 'test/'

metadata = []
for i in os.walk(PATH):
    x = i
x = x[-1]

for name in x:
    if '.txt' in name:
        arq = open(PATH + name, 'r')
        counts = get_metadata(arq)
        metadata.append(counts)
 
metadata = np.array(metadata)
sum_instances = np.sum(metadata, axis=0)
print('Total instances: ', sum_instances[0])
print('Car instances: ', sum_instances[1])
print('Bus instances: ', sum_instances[2])
print('Mot instances: ', sum_instances[3])


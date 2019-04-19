file = open('results.txt', 'r')

i = 0

print('pensando...')
while(1):
    prov = file.readline()
    if prov is '':
        break
    if 'Enter' in prov:
        new_file = open('frame{}.txt'.format(i), 'x')
        i += 1
    else:
        new_file.write(prov)

print('done!')



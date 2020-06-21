'''
    vou pegar o trainset e fazer k-trainsets,
                        cada um desse com um validset diferente,
                                                    escolhido aleatoriamente.
    pra isso vou usar a funcao Kfold do sklearn pra escolher os indices,
                                                            depois vou criar k-pastas com os novos trainsets
'''
from os import system
from sklearn.model_selection import KFold
import numpy as np

n_set = 433
ids = []
X_id = np.arange(0, n_set, 1)


kf = KFold(n_splits=4, shuffle=True)

for train_id, valid_id in kf.split(X_id):
    ids.append({'train_id': train_id, 'valid_id': valid_id})

for i in range(4):
    # criando os arquivos txt dos caminhos
    f1 = open("k{}/train.txt".format(i+1), 'w+')
    f2 = open("k{}/valid.txt".format(i+1), 'w+')

    for j in ids[i]['train_id']:
        system("cp fulltrain/frame{}.jpg k{}/train/".format(j, i+1))
        system("cp fulltrain/frame{}.txt k{}/train/".format(j, i+1))
        
        # caminho q vai ficar no colab etc
        f1.write("/content/darknet/data/k{}/train/frame{}.jpg\n".format(i+1, j))
    for k in ids[i]['valid_id']:
        system("cp fulltrain/frame{}.jpg k{}/valid/".format(k, i+1))
        system("cp fulltrain/frame{}.txt k{}/valid/".format(k, i+1))
        
        f2.write("/content/darknet/data/k{}/valid/frame{}.jpg\n".format(i+1, k))







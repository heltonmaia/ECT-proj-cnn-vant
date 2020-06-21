import pandas as pd
arq = open(input('digite o nome do arquivo: '), 'r')
tloss =[] 
avgloss = [] 
lrate = [] 
time = []


#cortando as strings e jogando os valores nas respectivas listas
while(1):
    prov = arq.readline()
    prov2 = []
    if ('avg loss' in prov):
        prov = prov.split(',')
        for i in range(len(prov)):
            prov2.append(prov[i].split(' '))
        tloss.append(float(prov2[0][2]))
        avgloss.append(float(prov2[1][1]))
        lrate.append(float(prov2[2][1]))
        time.append(float(prov2[3][1]))
    else:
        if prov == '':
            break


#criando e arrumando o dataframe
data = {'Total_loss': tloss,
            'Avg_loss': avgloss,
                'Learning rate': lrate,
                    'Time': time}
df = pd.DataFrame(data)
df.index.name = 'Epoch'
df.index += 1
df.to_csv(input('digite o nome do arquivo + .csv: '))




    


import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.patches as mp

#lendo os csvs dos treinos
tiny = pd.read_csv('tiny_logs.csv')
full = pd.read_csv('train_car_1_logs.csv')

#colocando em arrays
x_tiny = np.array(tiny["Iteration"])
y_tiny = np.array(tiny["Loss"])

x_full = np.array(full['Iteration'])
y_full = np.array(full['Loss'])

#criando legendas
red_patch = mp.Patch(color='red', label='Yolo')
blue_patch = mp.Patch(color='blue', label='Tiny Yolo')
plt.legend(handles=[red_patch, blue_patch])

#plot 
plt.plot(x_tiny, y_tiny, 'b')
plt.plot(x_full,y_full, 'r')
# doc das possibilidades de cores https://matplotlib.org/2.0.2/api/colors_api.html#module-matplotlib.colors

#labels
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training loss')

#marcacoes
plt.grid()

#limites do eixo y da figura
plt.ylim(top=8)
plt.ylim(bottom=0)

#showww
plt.show()


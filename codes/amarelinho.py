import cv2
import re
import numpy as np
import matplotlib.pyplot as plt
import math as m 
from random import *
from itertools import combinations

#recebe uma lista de veiculos e retorna uma lista com os pares
def get_pairs(lista):
    r = []
    for pair in combinations(lista, 2):
        r.append(pair)
    return r 


#recebe um par e um alfa(quanto de _d_, _dx_ tem que ser) e diz se
                                    #eh pra desenhar a distancia ou nao
def can_i_draw_it(pair, alfa=0.7):
    d = pair[0].get_norm(pair[1])
    dx = abs(pair[0].get_xdistances(pair[1]))
    if dx >= d*alfa:
        return True
    return False

#recebe um veic, uma lista de veics e um alfa(). retorna a dist
#          entre ele e o veic(da lista) mais perto dele
def mais_prox(obj, lista, alfa=0.998):
    dist = 999999
    for future in lista:
        prov = obj.get_mynorm(future)
        if prov < dist:
            dist = prov
            gon = future
    return dist, gon


#recebe 2 listas de veiculos. uma do frame anterior e outra do frame atual
#   insere as velocidades por 1 frame pra cada veiculo dao frame2
# OBS: ATE AGR SO FUNCIONA PRA 2 FRAMES COM O MSM NUMERO DE VEICULOS
def veloc_pframe(frame1, frame2):
    dists = []
    #lista friends. essa lista tem os veiculos do futuro que deram match com os veiculos do passado
    friends = []
    for obj in frame2:
        dist, friend = mais_prox(obj, frame1)
        #2 friends iguais na lista. verificar quem é fake
        if friend in friends:
            if obj.get_mynorm(friend) < frame1[friends.index(friend)].get_mynorm(friend):
                dists[friends.index(friend)] = 0.0
                dists.append(dist)
                friends.append(friend)
            else:
                dists.append(0.0)
                friends.append(obj)
        else:
                dists.append(dist)
                friends.append(friend)
    print('frame1 len: {}'.format(len(frame1)))
    print('frame2 len: {}'.format(len(frame2)))
    print('dists len: {}'.format(len(dists)))
    print('friends len: {}'.format(len(friends)))
                    
    for i in range(len(dists)):

        frame2[i].set_veloc(dists[i])
    return friends


class Veic():
    def __init__(self, argv):
        self.tipo = argv[0]
        self.prob = int(argv[1])
        self.width = int(argv[4]) 
        self.height = int(argv[5])
        self.x = int(argv[2])+int(self.width/2)
        self.y = int(argv[3])+int(self.height/2)
        self.veloc = 0.0
    def __str__(self):
        string = '{} ({}, {})'.format(self.tipo, self.x, self.y)
        return string
    def __repr__(self):
        string = '{} ({}, {})'.format(self.tipo, self.x, self.y)
        return string
    def get_Tipo(self):
        return self.tipo
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def get_height(self):
        return self.height
    def get_width(self):
        return self.width
    def get_prob(self):
        return self.prob
    def get_xdistances(self, obj):
        return abs(self.get_x() - obj.get_x())
    def get_ydistances(self, obj):
        return abs(self.get_y() - obj.get_y())


    #retorna a norma com um parametro beta [0,1] que perto de 0, dx tem mais influencia, e perto de 1, se aproxima da norma real     
    def get_mynorm(self, obj, beta=0.01):
        py = list(obj.get_point())
        py[1] = py[1]*beta
        px = list(self.get_point())
        px[1] = px[1]*beta

        return cv2.norm(tuple(px), tuple(py), cv2.NORM_L2)
    def get_norm(self, obj):
        return cv2.norm(self.get_point(), obj.get_point(), cv2.NORM_L2)
    
    
    def get_point(self):
        return (self.x, self.y)
    def get_veloc(self):
        return self.veloc
    def set_veloc(self, dpix):
        self.veloc = dpix
    def get_mid_point(self, obj):
        if self.x > obj.x:
            dx = (int(self.get_xdistances(obj)/2)) - self.x
        else:
            dx = (int(self.get_xdistances(obj)/2)) + self.x
        dy = int(abs(self.y + obj.get_y())/2)
        return (dx, dy)


def Remove(duplicate): 
    new = []
    for lin in duplicate: 
        if lin != '':
            new.append(lin)
    return new


#recebe um frame.txt do yolo e retorna uma lista de veiculos
def read(arqv):
    file = open(arqv, 'r')
    delimiters = "[:  ()\t'top_y''left_x''width''height'\n'%']"
    data = []
    while(1):
        prov = file.readline()
        if '%' in prov:
            prov = re.split(delimiters, prov)
            obj = []
            prov = Remove(prov)
            v = Veic(prov)
            for line in prov:
                if line != '':
                    obj.append(line)
                    
            data.append(v)    
        if prov == '':
            break
    return data


num_frames = 96
imgs = []

for i in range(num_frames):
    df1 = read('frames/frame{}.txt'.format(i))
    df2 = read('frames/frame{}.txt'.format(i+1))
    fig2 = cv2.imread('frames/frame{}.jpg'.format(i+1))
    for pair in get_pairs(df2):
        if can_i_draw_it(pair, alfa=0.996):
            #cv2.line(fig2, pair[0].get_point(), pair[1].get_point(), (0), 2)
            font = cv2.FONT_HERSHEY_SIMPLEX
            text_point1 = pair[0].get_mid_point(pair[1])
            print(text_point1)
            norm = pair[0].get_norm(pair[1])
            norm = str(norm)
            norm = norm[0:4]
            cv2.putText(fig2 ,norm, text_point1, font, .1,(20,150,255),1,cv2.LINE_AA)


    amigos = veloc_pframe(df1, df2)
    cont = 0
    cor = []
    for k in range(len(amigos)):
        prov = []
        prov.append(randint(0,255))
        prov.append(randint(0,255))
        prov.append(randint(0,255))
        cor.append(prov)

    for obj in df2:
        font = cv2.FONT_HERSHEY_SIMPLEX
        obj.y = obj.get_y() - 18
        text_point = obj.get_point()
        obj.y = obj.get_y() + 18

        veloc = obj.get_veloc()
        veloc = str(veloc)
        veloc = veloc[0:4]
        cv2.putText(fig2 ,veloc, text_point, font, 1,(25,155,0),4,cv2.LINE_AA)
        cv2.circle(fig2, amigos[cont].get_point(), 30, (0), 3)
        cv2.circle(fig2, obj.get_point(), 15, (0), 3)

        txt = str(amigos[cont].get_x()) +', ' + str(amigos[cont].get_y())
        #cv2.putText(fig2 , txt, amigos[cont].get_point(), font, 1,(0),4,cv2.LINE_AA)

        cont += 1



    imgs.append(fig2)



h, w, l = imgs[0].shape
size = (int(w), int(h))

video = cv2.VideoWriter('t.avi', cv2.VideoWriter_fourcc(*'DIVX'),15, size)
for i in range(len(imgs)):
    video.write(imgs[i])
video.release()






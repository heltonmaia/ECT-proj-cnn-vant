from random import *
from itertools import combinations

import cv2
import re
import numpy as np
import matplotlib.pyplot as plt
import math as m 
import os
import sys

def clear_text_output():
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[2K')

'''
Recebe um veic, uma lista de veics e um alfa(). retorna a distância entre ele e o veic(da lista) mais perto dele, e 
também o veic mais perto dele
'''
def mais_prox(obj, lista):
    dist = 999999
    gon = 0
    for future in lista:
        prov = obj.get_mynorm(future)
        if prov < dist:
            dist = prov
            gon = future
    return dist, gon


class Veic():
	# inicia com 1 array desse tipo: [class, score, x, y, width, height]
    def __init__(self, argv):
        self.tipo = argv[0]
        self.prob = int(argv[1])
        self.width = int(argv[4]) 
        self.height = int(argv[5])
        self.x = int(argv[2])+int(self.width/2)
        self.y = int(argv[3])+int(self.height/2)
        self.veloc = 0.0
        self.mean_veloc = 0.0
        self.time=0
        self.update_time = 15
    def __str__(self):
        string = '{} ({}, {})'.format(self.tipo, self.x, self.y)
        return string
    def __repr__(self):
        string = '{} ({}, {})'.format(self.tipo, self.x, self.y)
        return string
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def get_xdistances(self, obj):
        return abs(self.get_x() - obj.get_x())
    def get_ydistances(self, obj):
        return abs(self.get_y() - obj.get_y())
    def reset_veloc(self):
        self.veloc = 0.0
        '''
        get_mynorm: Recebe um objeto e retorna a norma entre esse objeto e o objeto que chamou a função. o parâmetro beta[0, 1] indica o peso que
        a coordenada y tem no calculo da norma. quando os veículos se movimentam apenas na horizontal, é interessante ter o beta perto do zero.
        '''   
    def get_mynorm(self, obj, beta=0.01):
        py = list(obj.get_point())
        py[1] = py[1]*beta
        px = list(self.get_point())
        px[1] = px[1]*beta

        return cv2.norm(tuple(px), tuple(py), cv2.NORM_L2)
    def get_norm(self, obj):
        return cv2.norm(self.get_point(), obj.get_point(), cv2.NORM_L2)
    def get_mean_veloc(self, time):
        return self.mean_veloc
    
    def get_point(self):
        return (self.x, self.y)
    def set_point(self, obj):
        p = obj.get_point()
        self.x = p[0]
        self.y = p[1]
    def get_veloc(self):
        return self.veloc
    def set_veloc(self, dpix):
        self.veloc += dpix
        self.time +=1
        if self.time ==1:
            self.mean_veloc = self.veloc
            self.time = 0
            self.veloc = 0.0
        


    def get_mid_point(self, obj):
        if self.x > obj.x:
            dx = (int(self.get_xdistances(obj)/2)) - self.x
        else:
            dx = (int(self.get_xdistances(obj)/2)) + self.x
        dy = int(abs(self.y + obj.get_y())/2)
        return (dx, dy)


class List_Veic():
    '''
    Lista de veiculos e a lista times que indica a quantidade de frames que um veiculo foi detectado tambem tem a lista 
    de veiculos que foram detectados e não estão mais aparecendo
    '''
    def __init__(self, frame):
        self.l = []
        self.times = []
        self.old = []
        self.last_positions = []
        self.mean_velocs = []
        for obj in frame:
            self.l.append(obj)
            self.times.append(0)
            self.mean_velocs.append(0.0)
    def set_frame(self, frame):
        dists = []
        pairs = []
        news = []
        old_obj = []
        for obj in frame:
            d, p = mais_prox(obj, self.l)
            if p in pairs:
                max_dist = max(d, dists[pairs.index(p)])        
                if max_dist == d:
                    news.append(obj)
                else:
                    news.append(p)
                    dists.remove(dists[pairs.index(p)])
                    pairs.remove(p)
            else:
                old_obj.append(obj)
                dists.append(d)
                pairs.append(p)
        '''
        Testando se nao tem nenhuma velocidade anormal. Caso seja, adicionamos esse veiculo aos novos e o removemos das listas pairs e dists
        '''
        for dist in dists:
            if dist > 28:
                self.l.append(pairs[dists.index(dist)])
                self.times.append(0)
                self.mean_velocs.append(0.0)
                pairs.remove(pairs[dists.index(dist)])
                dists.remove(dist)
        '''
        Agora vamos ver a relação entre os veiculos da lista pairs com os veiculos da lista self.l. Note que só será possivel ter 
        menos ou o mesmo numero de veiculos de self.l, na lista pairs
        '''
        to_remove = self.l.copy() # Lista dos veiculos de self.l que nao tiveram as suas velocidades atualizadas.
        for pair in pairs:
            to_remove.remove(self.l[self.l.index(pair)])
            self.last_positions.append(pair.get_point())
            self.l[self.l.index(pair)].set_veloc(dists[pairs.index(pair)])
            self.l[self.l.index(pair)].set_point(old_obj[pairs.index(pair)])
            self.times[self.l.index(pair)] += 1

        # Movendo os veiculos que sobraram para a lista dos veiculos que saíram do video
        if len(to_remove) != 0:
            for obj in to_remove:
                self.old.append(obj)
                self.times.remove(self.times[self.l.index(obj)])
                self.mean_velocs.remove(self.mean_velocs[self.l.index(obj)])
                self.l.remove(obj)
        for new in news:
            self.l.append(new)
            self.times.append(0)
            self.mean_velocs.append(0.0)
        


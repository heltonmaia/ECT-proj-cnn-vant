import cv2 as cv
import numpy as np

from scipy.spatial import distance
from collections import OrderedDict

class CentroidTracker():
    def __init__(self, maxDisappeared=30):
        # the id of the next object to be included
        self.nextObjectID = 0
       
        # dictionary like:
        #   {id: (centroid_x, centroid_y)}
        self.objects = OrderedDict()

        # dictionary like:
        #   {id: frames_disappeared}
        self.disappeared = OrderedDict()
        
        self.maxDisappeared = maxDisappeared

    def register(self, centroid):
        # register a centroid using the nextObjectID
        self.objects[self.nextObjectID] = centroid
        self.disappeared[self.nextObjectID] = 0
        self.nextObjectID += 1
    
    def deregister(self, objectID):
        # deregister a object from your id
        del self.objects[objectID]
        del self.disappeared[objectID]

    def update_centroid(self, id_, centroid):
        self.objects[id_] = centroid
        self.disappeared[id_] = 0
        
    def update(self, centroids):
        if len(centroids) == 0:
            #all objects disappear
            for objID in list(self.disappeared.keys):
                self.disappeared[objID] += 1
                if self.disappeared[objID] > self.maxDisappeared:
                    self.deregister(objID)
            return

        # register all centroids
        if len(self.objects) == 0:
            for centroid in centroids:
                self.register(centroid)

        else:
            objIDS = list(self.objects.keys())
            objs = list(self.objects.values())
            distances = distance.cdist(np.array(objs), centroids);
            
            minObjs = np.argmin(distances, axis=1);
    
            # vc pode pegar os minimos de cada linha
            # dps vc registra os valores unicos
            # dps vc da sort nos que sobraram com o msm indice
            # a lista distances sera util
            
            idx_to_update, idx_centroids = [], []

            # vai adicionando os centroids novos dos respectivos objetos
            # se ja tiver tiver alguma repeticao confere qual eh o menor e bota o menor
            for obj_idx, cent_idx in enumerate(minObjs):
                if cent_idx not in idx_centroids:
                    idx_to_update.append(obj_idx)
                    idx_centroids.append(cent_idx)
                else:
                    repeated_obj = idx_to_update[idx_centroids.index(cent_idx)]
                    previous_distance = distances[repeated_obj, cent_idx]
                    if min(distances[obj_idx, cent_idx], previous_distance) != previous_distance:
                        idx_to_update.remove(repeated_obj)
                        idx_centroids.remove(cent_idx)
                        idx_to_update.append(obj_idx)
                        idx_centroids.append(cent_idx)

            # dando update
            for updt_idx, cent_idx in zip(idx_to_update, idx_centroids):
                self.update_centroid(updt_idx, centroids[cent_idx]) 

            # agora precisa conferir quais objs nao tiveram centroids novos associados
            # ou seja qual obj da lista objs nao esta em idx_to_update
            # se for o caso, aumenta o maxdisappeared or remove
            for obj_idx in range(len(objs)):
                if obj_idx not in idx_centroids:
                    self.disappeared[objIDS[obj_idx]] += 1
                    if self.disappeared[objIDS[obj_idx]] > self.maxDisappeared:
                        self.deregister(objIDS[obj_idx])

            # if dont have objects which match distance with an input centroid, then this centroid is a new object
            for centroidIdx, centroid in enumerate(centroids):
                if centroidIdx not in minObjs:
                    self.register(centroid)

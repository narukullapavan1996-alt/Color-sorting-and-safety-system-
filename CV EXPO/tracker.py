import numpy as np
from collections import defaultdict

class CentroidTracker:
    def __init__(self, maxDisappeared=40, maxTrailLength=15):
        self.nextObjectID = 0
        self.objects = {}
        self.disappeared = {}
        self.trails = defaultdict(list)
        self.velocity = {}
        self.shapes = {}
        self.maxDisappeared = maxDisappeared
        self.maxTrailLength = maxTrailLength

    def register(self, centroid, shape):
        self.objects[self.nextObjectID] = centroid
        self.disappeared[self.nextObjectID] = 0
        self.trails[self.nextObjectID] = [centroid]
        self.velocity[self.nextObjectID] = 0.0
        self.shapes[self.nextObjectID] = shape
        self.nextObjectID += 1

    def deregister(self, objectID):
        del self.objects[objectID]; del self.disappeared[objectID]
        del self.trails[objectID]; del self.velocity[objectID]
        del self.shapes[objectID]

    def update(self, rects, detected_shapes):
        if len(rects) == 0:
            for objID in list(self.disappeared.keys()):
                self.disappeared[objID] += 1
                if self.disappeared[objID] > self.maxDisappeared: self.deregister(objID)
            return self.objects

        inputCentroids = np.array([(r[0] + r[2]//2, r[1] + r[3]//2) for r in rects])
        
        if len(self.objects) == 0:
            for i in range(len(inputCentroids)): 
                self.register(inputCentroids[i], detected_shapes[i])
        else:
            objectIDs = list(self.objects.keys()); objectCentroids = list(self.objects.values())
            D = np.linalg.norm(np.array(objectCentroids)[:, np.newaxis] - inputCentroids, axis=2)
            rows = D.min(axis=1).argsort(); cols = D.argmin(axis=1)[rows]
            usedRows, usedCols = set(), set()
            
            for (row, col) in zip(rows, cols):
                if row in usedRows or col in usedCols or D[row, col] > 75: continue
                objID = objectIDs[row]
                new_c = inputCentroids[col]
                
                self.velocity[objID] = round(np.linalg.norm(new_c - self.objects[objID]), 1)
                self.objects[objID] = new_c
                self.shapes[objID] = detected_shapes[col]
                self.disappeared[objID] = 0
                self.trails[objID].append(new_c)
                
                if len(self.trails[objID]) > self.maxTrailLength: 
                    self.trails[objID] = self.trails[objID][-self.maxTrailLength:]
                usedRows.add(row); usedCols.add(col)
                
            for col in set(range(len(inputCentroids))).difference(usedCols): 
                self.register(inputCentroids[col], detected_shapes[col])
                
            for row in set(range(len(objectCentroids))).difference(usedRows):
                objID = objectIDs[row]; self.disappeared[objID] += 1
                if self.disappeared[objID] > self.maxDisappeared: self.deregister(objID)
                
        return self.objects
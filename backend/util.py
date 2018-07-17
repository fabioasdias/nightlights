import tempfile
import zipfile
import shutil
import geojson
from glob import glob
from os.path import basename
from rtree import index
from shapely.geometry import shape, MultiPolygon
from shapely.ops import snap
from geojson import Feature, FeatureCollection
from copy import deepcopy
import json


class indexedPols:
    def __init__(self):
        self._index = index.Index()
        self._pols = []
        self._removed = [] #each polygon has a allocated value - more memory, but faster
        self._properties = {}

    def __next__(self):
        for i in range(len(self._pols)):
            if not self._removed[i]:
                yield(self._pols[i])

    def __iter__(self):
        return(next(self))
        
    def getProps(self,polID):
        return(self._properties[polID])
    def getProperty(self,polID,prop='CT_ID'):
        return(self._properties[polID][prop])

    def iterIDGeom(self,idfield='CT_ID'):
        """Returns a generator that goes over the geometries, 
           returning them along the property named by idfield"""
        for i in range(len(self._pols)):
            if not self._removed[i]:
                yield(self._properties[i][idfield],self._pols[i])
    def getPolygon(self,polID):
        return(self._pols[polID])

    def insert(self,g,props={}):
        if (not g) or (not g.bounds):
            return
        self._index.insert(len(self._pols),g.bounds)
        self._properties[len(self._pols)]=deepcopy(props)
        self._pols.append(deepcopy(g))
        self._removed.append(False)

    def bbSearch(self,geom):
        if (len(self._pols)==0):
            return([])
        return([i for i in self._index.intersection(geom.bounds) if (not self._removed[i])])        

    def containedIn(self,geom):
        if (len(self._pols)==0):
            return([])
        res=[]
        for i in self._index.intersection(geom.bounds):
            if (not self._removed[i]) and (geom.contains(self._pols[i])):
                res.append(i)
        return(res)        

    def search(self,geom):
        if (len(self._pols)==0) or (geom.is_empty):
            return([])
        res=[]

        for i in self._index.intersection(geom.bounds):
            if (not self._removed[i]) and (geom.intersects(self._pols[i])):
                res.append(i)
        return(res)        
    
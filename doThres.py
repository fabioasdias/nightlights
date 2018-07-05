import ogr, gdal, osr, os
import numpy as np
import itertools
from math import sqrt,ceil
import scipy as sp
import scipy.ndimage as ni
from skimage.morphology import diamond
import sys
import matplotlib.pylab as plt
from skimage.filters import threshold_otsu,gaussian
from skimage.measure import find_contours
from os.path import exists
import inspect

#https://stackoverflow.com/a/37312185/5129009
def bbox(img,l):
    img = (img == l)
    rows = np.any(img, axis=1)
    cols = np.any(img, axis=0)
    rmin, rmax = np.argmax(rows), img.shape[0] - 1 - np.argmax(np.flipud(rows))
    cmin, cmax = np.argmax(cols), img.shape[1] - 1 - np.argmax(np.flipud(cols))
    return(rmin, rmax, cmin, cmax)

def pixelOffset2coord(rasterfn,xOffset,yOffset):
    raster = gdal.Open(rasterfn)
    geotransform = raster.GetGeoTransform()
    originX = geotransform[0]
    originY = geotransform[3]
    pixelWidth = geotransform[1]
    pixelHeight = geotransform[5]
    coordX = originX+pixelWidth*xOffset
    coordY = originY+pixelHeight*yOffset
    return coordX, coordY

def raster2array(rasterfn):
    raster = gdal.Open(rasterfn)
    band = raster.GetRasterBand(1)
    array = band.ReadAsArray()
    return array

def array2shp(array,outSHPfn,rasterfn,pixelValue):

    # max distance between points
    raster = gdal.Open(rasterfn)
    geotransform = raster.GetGeoTransform()
    pixelWidth = geotransform[1]
    maxDistance = ceil(sqrt(2*pixelWidth*pixelWidth))
    print(maxDistance)

    # array2dict
    count = 0
    roadList = np.where(array == pixelValue)
    multipoint = ogr.Geometry(ogr.wkbMultiLineString)
    pointDict = {}
    for indexY in roadList[0]:
        indexX = roadList[1][count]
        Xcoord, Ycoord = pixelOffset2coord(rasterfn,indexX,indexY)
        pointDict[count] = (Xcoord, Ycoord)
        count += 1

    # dict2wkbMultiLineString
    multiline = ogr.Geometry(ogr.wkbMultiLineString)
    for i in itertools.combinations(pointDict.values(), 2):
        point1 = ogr.Geometry(ogr.wkbPoint)
        point1.AddPoint(i[0][0],i[0][1])
        point2 = ogr.Geometry(ogr.wkbPoint)
        point2.AddPoint(i[1][0],i[1][1])

        distance = point1.Distance(point2)

        if distance < maxDistance:
            line = ogr.Geometry(ogr.wkbLineString)
            line.AddPoint(i[0][0],i[0][1])
            line.AddPoint(i[1][0],i[1][1])
            multiline.AddGeometry(line)

    # wkbMultiLineString2shp
    shpDriver = ogr.GetDriverByName("ESRI Shapefile")
    if os.path.exists(outSHPfn):
        shpDriver.DeleteDataSource(outSHPfn)
    outDataSource = shpDriver.CreateDataSource(outSHPfn)
    outLayer = outDataSource.CreateLayer(outSHPfn, geom_type=ogr.wkbMultiLineString )
    featureDefn = outLayer.GetLayerDefn()
    outFeature = ogr.Feature(featureDefn)
    outFeature.SetGeometry(multiline)
    outLayer.CreateFeature(outFeature)

def closing(img,s):
    ret=ni.maximum_filter(img,footprint=diamond(s))
    ret=ni.minimum_filter(ret,footprint=diamond(s))
    return(ret)
def opening(img,s):
    ret=ni.minimum_filter(img,footprint=diamond(s))
    ret=ni.maximum_filter(ret,footprint=diamond(s))
    return(ret)
def ASF(img,s):
    ret=img.copy()
    for i in range(1,s):
        print(i)
        ret=closing(ret,i)
        ret=opening(ret,i)
    return(ret)

    

def main(rasterfn,outSHPfn):
    
    array = raster2array(rasterfn)
    array = np.where(array>1,np.log(array),0)

    centre=[8584, 25030]
    delta= 1000
    array=array[centre[0]-delta:centre[0]+delta,centre[1]-delta:centre[1]+delta]
    array=ni.maximum_filter(array,footprint=diamond(1))

    nASF=20
    cacheName='{0}_asf'.format(nASF)+rasterfn.replace('tif','_marker.npy')

    if (exists(cacheName)):
        print('loading asf')
        with open(cacheName, 'rb') as f:
            marker = np.load(f)
    else:    
        marker=ASF(array,nASF)
        with open(cacheName, 'wb') as f:
            np.save(f,marker)                
    
    T=threshold_otsu(marker)
    marker=np.where(marker<T,0,1)
    labels, NL=ni.label(marker)
    print("Regions: ",NL)
    
    for i in range(1,NL+1):
        print(i)
        xmin,xmax,ymin,ymax=bbox(labels,i)
        dx=int(0.3*np.abs(xmin-xmax))
        dy=int(0.3*np.abs(ymin-ymax))
        xmin=np.max((xmin-dx,0))
        xmax=np.min((xmax+dx,marker.shape[0]))
        ymin=np.max((ymin-dy,0))
        ymax=np.min((ymax+dy,marker.shape[1]))
        base=array[xmin:xmax,ymin:ymax]

        base=(base-np.min(base))/(np.max(base)-np.min(base))
        base=gaussian(base,5)
        init=labels[xmin:xmax,ymin:ymax]
        init=np.where(init==i,1,0)        
        newInit=np.zeros((init.shape[0]+2,init.shape[1]+2))
        newInit[1:-1,1:-1]=init
        init=find_contours(newInit,0.5)[0]
        init=init[::5,:]-1


        plt.figure()
        plt.imshow(base)
        plt.colorbar()
        
        plt.plot(init[:,1],init[:,0],'.-b')


        plt.show()






if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])
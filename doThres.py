import ogr, gdal, osr, os
import numpy as np
import itertools
from math import sqrt,ceil
import scipy as sp
import scipy.ndimage
from skimage.morphology import diamond
import sys
import matplotlib.pylab as plt
from skimage.filters import threshold_otsu
from os.path import exists

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
    ret=sp.ndimage.maximum_filter(img,footprint=diamond(s))
    ret=sp.ndimage.minimum_filter(ret,footprint=diamond(s))
    return(ret)
def opening(img,s):
    ret=sp.ndimage.minimum_filter(img,footprint=diamond(s))
    ret=sp.ndimage.maximum_filter(ret,footprint=diamond(s))
    return(ret)
def ASF(img,s):
    ret=img.copy()
    for i in range(1,s):
        print(i)
        ret=closing(ret,i)
        ret=opening(ret,i)
    return(ret)

    

def main(rasterfn,outSHPfn):
    cacheName=rasterfn.replace('tif','_marker.npy')
    array = raster2array(rasterfn)
    array = np.where(array>1,np.log(array),0)

    if (exists(cacheName)) and False:
        with open(cacheName, 'rb') as f:
            marker = np.load(f)
    else:
        centre=[8584, 24530]
        delta= 750
        array=array[centre[0]-delta:centre[0]+delta,centre[1]-delta:centre[1]+delta]
        marker=ASF(array,10)
        # with open(cacheName, 'wb') as f:
        #     np.save(f,marker)
                
    plt.figure()
    plt.imshow(array)
    plt.colorbar()

    
    T=threshold_otsu(marker)
    print(T)
    marker=np.where(marker<T,0,1)

    plt.figure()
    plt.imshow(marker)
    plt.colorbar()


    plt.show()
    exit()
    # RELEVANT LINES: check if pixel belongs to border
    imax=(sp.ndimage.maximum_filter(array,size=3)!=array)
    imin=(sp.ndimage.minimum_filter(array,size=3)!=array)
    icomb=np.logical_or(imax,imin)

    # keep only pixels of original array at borders
    edges=np.where(icomb,-1,0)
    # toview=rescale(edges,0.1)
    # plt.imshow(toview)
    # plt.colorbar()
    # plt.show()
    array2shp(edges,outSHPfn,rasterfn,-1)#-1 => watershed marker

if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])
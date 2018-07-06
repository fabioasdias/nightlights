import gdal, osr
import numpy as np
from scipy.ndimage import maximum_filter
import sys
from skimage.filters import gaussian,threshold_li
from skimage.measure import find_contours
from scipy.ndimage import maximum_filter,minimum_filter
from os.path import exists
import inspect
import json

DEBUG = True
if DEBUG:
    import matplotlib.pylab as plt

#https://stackoverflow.com/a/37312185/5129009
def bbox(img,l):
    img = (img == l)
    rows = np.any(img, axis=1)
    cols = np.any(img, axis=0)
    rmin, rmax = np.argmax(rows), img.shape[0] - 1 - np.argmax(np.flipud(rows))
    cmin, cmax = np.argmax(cols), img.shape[1] - 1 - np.argmax(np.flipud(cols))
    return(rmin, rmax, cmin, cmax)

#https://stackoverflow.com/questions/50191648/gis-geotiff-gdal-python-how-to-get-coordinates-from-pixel/50196761
def pixelOffset2coord(geotransform,t,x,y):
    originX = geotransform[0]
    originY = geotransform[3]
    pixelWidth = geotransform[1]
    pixelHeight = geotransform[5]
    posX = originX+pixelWidth*x
    posY = originY+pixelHeight*y
    (lat, lon, z) = t.TransformPoint(posX, posY)
    return lat,lon

def main(rasterfn,outGJ):
    raster = gdal.Open(rasterfn)
    crs = osr.SpatialReference()
    crs.ImportFromWkt(raster.GetProjectionRef())
    # create lat/long crs with WGS84 datum
    crsGeo = osr.SpatialReference()
    crsGeo.ImportFromEPSG(4326) # 4326 is the EPSG id of lat/long crs 
    t = osr.CoordinateTransformation(crs, crsGeo)
    geotransform = raster.GetGeoTransform()
    band = raster.GetRasterBand(1)
    array = band.ReadAsArray()
    band = None
    raster = None
    # array = np.where(array>1,np.log(array),0)

    if DEBUG:
        centre=[8000,25500]                
        delta= [1000,1000]
        minx=centre[0]-delta[0]
        maxx=centre[0]+delta[1]
        miny=centre[1]-delta[0]
        maxy=centre[1]+delta[1]
        mask=(slice(minx,maxx),slice(miny,maxy),)
        plt.figure(1)
        plt.imshow(array[mask])
        plt.title('Original data NOAA')
        plt.colorbar()
        plt.figure(2)
        plt.imshow(np.where(array[mask]>1,np.log(array[mask]),0).T,extent=[minx,maxx,miny,maxy],origin='lower')
        plt.title('log data NOAA')
        plt.colorbar()


    # amin=np.min(array)
    # amax=np.max(array)
    # array=(array-amin)/(amax-amin)
    T=6#threshold_li(array)
    array = np.where(array<=T,0.0,1.0)
    array = maximum_filter(array,size=9)
    # array = minimum_filter(array,size=32)
    if DEBUG:
        plt.figure()
        plt.imshow(array[mask])
        plt.title('Adaptive threshold (li) {0:.2f}'.format(T))
        plt.colorbar()

    array = gaussian(array,16)
    array = array/np.max(array)
    if DEBUG:
        plt.figure()
        plt.imshow(array[mask])
        plt.title('Gaussian smoothing')
        plt.colorbar()

    res={}
    res["type"]="FeatureCollection"
    res["features"]=[]        

    for c in find_contours(array,0.5):
        coordinates=[]
        if DEBUG:
            plt.figure(2)
            plt.plot(c[:,0],c[:,1])

        for i in range(c.shape[0]):
            lat,lon=pixelOffset2coord(geotransform,t,c[i,1],c[i,0])
            coordinates.append([lat,lon])

        res["features"].append({
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [coordinates,]
            },
        "properties": {}
        })
    with open(outGJ,'w') as f:
        json.dump(res,f)


    if DEBUG:
        plt.show()
  
    

if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])
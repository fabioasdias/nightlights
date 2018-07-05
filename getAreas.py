import gdal, osr
import numpy as np
from scipy.ndimage import maximum_filter
import sys
from skimage.filters import gaussian,threshold_otsu
from skimage.measure import find_contours
from os.path import exists
import inspect
import json

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
    array = np.where(array>1,np.log(array),0)

        
    # delta= 5000
    # array=array[:delta,:delta]

    amin=np.min(array)
    amax=np.max(array)
    array=(array-amin)/(amax-amin)
    array=maximum_filter(array,size=3)
    array = gaussian(array,32)
    

    res={}
    res["type"]="FeatureCollection"
    res["features"]=[]
    T=threshold_otsu(array)
    for c in find_contours(array,T):
        coordinates=[]
        for i in range(c.shape[0]):
            lat,lon=pixelOffset2coord(geotransform,t,c[i,1],c[i,0])
            coordinates.append([lat,lon])

        res["features"].append({
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [coordinates,]
            },
        "properties": {'nothing':0}
        })
    with open(outGJ,'w') as f:
        json.dump(res,f)
  
    

if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])
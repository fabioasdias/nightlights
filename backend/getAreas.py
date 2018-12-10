import gdal, osr
import numpy as np
from scipy.ndimage import maximum_filter
from shapely.geometry import shape, mapping, Polygon
import sys
from skimage.filters import gaussian,threshold_li
from skimage.measure import find_contours
from skimage.morphology import diamond
from scipy.ndimage import maximum_filter,minimum_filter
from os.path import exists
import inspect
import json
from glob import glob

# DEBUG = True
DEBUG = False
DEBUG_RESCALE = False
if DEBUG:
    import matplotlib.pylab as plt
    from skimage.transform import rescale

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
    possibleFiles=list(glob(rasterfn))
    if (not possibleFiles):
        print('file not found')
        exit(-1)
    
    raster = gdal.Open(possibleFiles[0])
    crs = osr.SpatialReference()
    crs.ImportFromWkt(raster.GetProjectionRef())
    # create lat/long crs with WGS84 datum
    crsGeo = osr.SpatialReference()
    crsGeo.ImportFromEPSG(4326) # 4326 is the EPSG id of lat/long crs 
    t = osr.CoordinateTransformation(crs, crsGeo)
    geotransform = raster.GetGeoTransform()
    band = raster.GetRasterBand(1)
    array = band.ReadAsArray()
    print(possibleFiles[0],array.shape)
    band = None
    raster = None
    # array = np.where(array>1,np.log(array),0)

    if DEBUG:
        centre=[8200,25500]  # east
        # centre=[7000,13500] #west          
        delta= [500,500]
        minx=np.max((0,centre[0]-delta[0]))
        maxx=np.min((array.shape[0],centre[0]+delta[1]))
        miny=np.max((0,centre[1]-delta[0]))
        maxy=np.min((array.shape[1],centre[1]+delta[1]))
        # minx=4000
        # maxx=12100
        # miny=13200
        # maxy=27000
        mask=(slice(minx,maxx),slice(miny,maxy),)
        
        # plt.imshow(np.where(array[mask]>1,np.log(array[mask]),0))
        if (DEBUG_RESCALE):
            plt.figure(2)            
            aux=np.where(array>1,np.log(array),0).T
            aux=aux/np.max(aux)
            small=rescale(aux,0.2)
            del(aux)
            plt.imshow(small,extent=[0,array.shape[0],0,array.shape[1]],origin='lower')
            plt.title('log data NOAA')
            plt.colorbar()
            plt.xticks([])
            plt.yticks([])

        else:
            plt.figure(1)
            plt.imshow(array[mask])
            plt.title('Original data NOAA')
            plt.colorbar()
            plt.xticks([])
            plt.yticks([])

        # plt.show()

    # amin=np.min(array)
    # amax=np.max(array)
    # array=(array-amin)/(amax-amin)
    T=1
    array = np.where(array<=T,array/T,1.0)
    if DEBUG:
        if (not DEBUG_RESCALE):
            plt.figure()
            plt.imshow(array[mask])
            plt.title('threshold {0:.2f}'.format(T))
            plt.colorbar()
            plt.xticks([])
            plt.yticks([])


    # array = minimum_filter(array,size=3)
    # array = maximum_filter(array,size=5)#footprint=diamond(9))
    # array = minimum_filter(array,size=9)
    if DEBUG:
        if (not DEBUG_RESCALE):
            plt.figure()
            plt.imshow(array[mask])
            plt.title('threshold {0:.2f} + dilation square 5'.format(T))
            plt.colorbar()
            plt.xticks([])
            plt.yticks([])


    array = gaussian(array,24)
    array = array/np.max(array)
    if DEBUG:
        if DEBUG_RESCALE:
            small=rescale(array,0.2)
            plt.figure()
            plt.imshow(small)
            plt.title('Gaussian smoothing')
            plt.colorbar()
            plt.savefig(outGJ+'.gauss.png',dpi=900)
            plt.close()
        else:
            plt.figure(4)
            plt.imshow(array[mask])#,extent=[minx,maxx,miny,maxy],origin='lower')
            plt.title('Gaussian smoothing')
            plt.colorbar()
            plt.xticks([])
            plt.yticks([])
            plt.show()


    spots=[]
    # holes={}
    for c in find_contours(array,0.25):
        coordinates=[]
        # if DEBUG:
        #     plt.figure(4)
        #     plt.plot(c[:,0],c[:,1],'k-',linewidth=0.25)

        for i in range(c.shape[0]):
            lat,lon=pixelOffset2coord(geotransform,t,c[i,1],c[i,0])
            coordinates.append((lat,lon))
        geom=Polygon(coordinates)
        # if (geom.area<1):
        #     continue
        intersect=False
        for i in range(len(spots)):
            if (spots[i].contains(geom)):
                # if (i not in holes):
                #     holes[i]=[]
                # holes[i].append(geom)
                intersect=True
                break
        if not intersect:
            spots.append(geom)

    
    # for i in holes:
    #     spots[i]=Polygon(spots[i],holes=holes[i])


    res={}
    res["type"]="FeatureCollection"
    res["features"]=[]        

    for s in spots:
        res["features"].append({
        "type": "Feature",
        "geometry": mapping(s),
        "properties": {}
        })
        
    with open(outGJ,'w') as f:
        json.dump(res,f)


    if DEBUG:
        # plt.savefig(outGJ+'.areas.png',dpi=900)
        # plt.close()
        plt.figure(4)
        plt.show()
  
    

if __name__ == "__main__":
    main(sys.argv[1],sys.argv[2])

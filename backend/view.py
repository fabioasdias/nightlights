import georaster
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import sys

fig = plt.figure(figsize=(8,8))

# full path to the geotiff file
fpath = sys.argv[1]

# read extent of image without loading
# good for values in degrees lat/long
# geotiff may use other coordinates and projection
my_image = georaster.SingleBandRaster(fpath, load_data=False)

# grab limits of image's extent
minx, maxx, miny, maxy = my_image.extent

# set Basemap with slightly larger extents
# set resolution at intermediate level "i"
m = Basemap( projection='cyl', \
            llcrnrlon=minx-2, \
            llcrnrlat=miny-2, \
            urcrnrlon=maxx+2, \
            urcrnrlat=maxy+2, \
            resolution='i')

m.drawcoastlines(color="gray")
# m.fillcontinents(color='beige')

# load the geotiff image, assign it a variable
image = georaster.SingleBandRaster( fpath, \
                        load_data=(minx, maxx, miny, maxy), \
                        latlon=True)

# plot the image on matplotlib active axes
# set zorder to put the image on top of coastlines and continent areas
# set alpha to let the hidden graphics show through
plt.imshow(image.r, extent=(minx, maxx, miny, maxy), zorder=10, alpha=0.9) #
plt.colorbar()

plt.show()
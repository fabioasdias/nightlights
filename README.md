# Nightlights

Original satellite data from <a target="_blank" rel="noopener noreferrer" href="https://ngdc.noaa.gov/eog/viirs/download_dnb_composites.html"> the Earth Observation Group, NOAA National Geophysical Data Center</a>.

We use the annual composite of the VIIRS Day/Night Band Nighttime Lights to detect conurbation between metropolitan regions. 

## Article using this data/method at citylab:
https://www.citylab.com/life/2019/02/global-megaregions-economic-powerhouse-megalopolis/583729/

An analysis using this data has been published in [TESG](https://onlinelibrary.wiley.com/doi/pdf/10.1111/tesg.12449)

## Interactive visualization:
[Link to the interface](https://fabioasdias.github.io/nightlights/)

In this visualization, we represent a clipped version of the log of the satellite data. The original data is too spiky to see anything directly. The borders of the mega regions encompassing more than one metro region are represented in red. 

## Summary of the algorithm:

1. Binarization of the original data using a threshold of 1 nanoWatts/cm2/sr. 
1. <a target="_blank" rel="noopener noreferrer"  href="https://en.wikipedia.org/wiki/Dilation_(morphology)"> Morphological dilation</a> with a square structuring element of size 5.
1. <a target="_blank" rel="noopener noreferrer"  href="https://docs.scipy.org/doc/scipy-0.16.1/reference/generated/scipy.ndimage.filters.gaussian_filter.html">Gaussian filter of size 32</a> to smooth the data.
1. Rescale the data to 0-1 (divide by maximum).
1. <a target="_blank" rel="noopener noreferrer"   href="http://scikit-image.org/docs/dev/api/skimage.measure.html#skimage.measure.find_contours"> Find the contour lines</a> for level 0.5.

For more details, check the [source file](../master/backend/getAreas.py).
 
 

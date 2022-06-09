#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 16:05:07 2018

@author: koenig.g
"""

####################################
# Script to draw a rectangular map #
# of New-Caledonia. Inspired from  #
# Examples of cartopy. By Guillaume#
# Koenig, the 6/04/2018            #
####################################

#******Packages Import*************#
import matplotlib.pyplot as plt
import numpy as np

import cartopy
import cartopy.crs as ccrs

#********Figure and image***********#

Google_Image = cimgt.OSM() # Load the repertory of images from Open Street Maps
fig=plt.figure(figsize=(12,12)) # Create a figure with a given size
ax = plt.axes(projection=ccrs.PlateCarree()) # Create a GeoAxes in the tile's projection.
ax.stock_img() # Uses a stock image as background

# Limit the extent of the map to a small longitude/latitude range.
ax.set_extent([162., 169., -24., -19.], crs=ccrs.PlateCarree())

ax.add_feature(cartopy.feature.OCEAN, zorder=0) # Draw Ocean
ax.add_feature(cartopy.feature.LAND, zorder=0, edgecolor='black') # Draw land

plt.show()

fig.savefig('New_Caledonia_1.png')

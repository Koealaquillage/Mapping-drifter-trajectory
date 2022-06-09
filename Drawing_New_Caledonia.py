#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 15:58:32 2018

@author: koenig.g
"""

#*********************************************#
# Script to draw an Earthglobe centered on    #
# New-Caledonia. Taken from the examples of   #
# Cartopy. By Guillaume Koenig, the 06/04/2018#
###############################################

#***********Packages Import*******************#
import matplotlib.pyplot as plt
import numpy as np

import cartopy
import cartopy.crs as ccrs

#**********Figure and canvas declarations******#
fig=plt.figure(figsize=(12,12))
ax = plt.axes(projection=ccrs.Orthographic(164.5, -21.))

#**********Drawing*****************************#
ax.add_feature(cartopy.feature.OCEAN, zorder=0) #Blue Patch for the Ocean
ax.add_feature(cartopy.feature.LAND, zorder=0, edgecolor='black') # Yellow Patch for land

ax.set_global() # Define the limits of the ax as half a globe
ax.gridlines() # Plot the lat/lon lines

plt.show() # Show the graph

fig.savefig('New_Caledonia.png') # Save the graph

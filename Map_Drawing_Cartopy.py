####################################
# Script to draw  a map of Kone    #
# Using cartopy and google images  #
# With our drifter data.           #
# By Guillaume Koenig, the 27/02   #
# Very strongly inspired from :    #
# http://scitools.org.uk/cartopy/  #
# docs/v0.15/examples/             #
# eyja_volcano.html                #
# 19/04/2018 : This version has    #
# Trouble downloading the image    #
# From Google's servers ( Koenig.G)#
####################################

#**********Packages Import*********#

import matplotlib.pyplot as plt
from matplotlib.transforms import offset_copy

import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt

import pandas as pd
import matplotlib.cm as cm
import numpy as np

import Lib_Ext_Cartopy
#********Input Data variables*********#

# We're gonna create three list to store : The data, the size and the associated colormap
Drift_3=[None]*3
Kone_1=[None]*3
Kone_2=[None]*3

# And of course, a list and a dictionnary to loop on it

Lib_Drift=['Drift3','Kone1','Kone2']  

Dict_Drift={'Drift3':Drift_3,'Kone1':Kone_1,'Kone2':Kone_2}


#**********Data Import***************#

for FOO in Lib_Drift:
    # First we import the data
    Dict_Drift[FOO][0]=pd.read_csv('../DONNEES/spot_messages_'+FOO+'.csv',usecols=[0,2,3,4],
                    parse_dates=[0],names=['Datetime','Status','lat','lon'],index_col=[0])
    
    # Then we get the size
    Dict_Drift[FOO][1]=Dict_Drift[FOO][0].lon.size
    
# Now we have to get the colormaps separately

#Drift_3,shades of red 
Drift_3[2]=cm.Reds(np.linspace(1,0,Drift_3[1]+70))

#Kone_1,shades of purple
Kone_1[2]=cm.Purples(np.linspace(1,0,Kone_1[1]+1500))

#Kone_2,shades of green
Kone_2[2]=cm.Greens(np.linspace(1,0,Drift_3[1]+70))

#***********Map Drawing*****************#

# Download a google map satellite image
Google_Image = cimgt.OSM()

# Create a figure
fig=plt.figure(figsize=(12,8))
# Create a GeoAxes in the tile's projection.
ax = fig.add_subplot(1, 1, 1, projection=Google_Image.crs)

# Limit the extent of the map to a small longitude/latitude range.
ax.set_extent([164.35, 164.9, -21.14, -20.86], crs=ccrs.Geodetic())
#ax.set_extent([164, 180, -25, -20], crs=ccrs.Geodetic())

# Add the Google_Image at zoom level 12.
ax.add_image(Google_Image, 12)

#****Adding elements to the map*******#

# Add a marker for the nickel refinery
#ax.plot(164.68, -21.01, marker='o', color='blue', markersize=12,
#        alpha=0.9, transform=ccrs.Geodetic())


# Add text 25 pixels to the left of the volcano.
#ax.text(164.6, -21.01, 'Raffinerie de Nickel',
#        verticalalignment='center', horizontalalignment='right',
#           bbox=dict(facecolor='sandybrown', alpha=0.5, boxstyle='round'))

# Add meridians and parallels
ax.gridlines(draw_labels=True)

ax.set_xlabel('Longitude (degres Est)')
ax.set_ylabel('Latitude (degres Sud)')
   
#****Putting the data****************#

for FOO in Lib_Drift:
    ax.scatter(Dict_Drift[FOO][0].lon,Dict_Drift[FOO][0].lat,transform=ccrs.Geodetic(),
                   alpha=0.5,s=5,color=Dict_Drift[FOO][2],label=FOO)


ax.legend(loc='lower right')

fig=ax.get_figure() # Attribute the figure on which the ax is plotted to a variable

fig.show()
fig.savefig('Kone_Lagoon.jpeg')

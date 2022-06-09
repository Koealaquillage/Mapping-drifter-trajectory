#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 13:59:55 2018

@author: koenig.g
"""

##########################################
# Script to draw a map of the Kone Lagoon#
# But in a clean way. By Guillaume Koenig#
# The 12/04/2018                         #
##########################################

#****Packages Import***#

import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import pandas as pd

import Lib_Ext_Cartopy # My library with my external functions
#****Function***********#

 
#**********Data Import***************#
  
# Create three empty arrays to store data  
Drift_3=[]
Kone_1=[]
Kone_2=[]

# And of course, a list

Lib_Drift=['Kone1','Kone2']  

# And two dictionaries to loop on and attribute colors
Dict_Drift={'Drift3':Drift_3,'Kone1':Kone_1,'Kone2':Kone_2}
Dict_color={'Drift3':'red','Kone1':'orange','Kone2':'blue'}

#**********Data Import***************#

for FOO in Lib_Drift:
    Dict_Drift[FOO]=pd.read_csv('../DONNEES/spot_messages_'+FOO+'.csv',usecols=[0,2,3,4],
                    parse_dates=[0],names=['Datetime','Status','lat','lon'],index_col=[0])

    # Now I have to reverse the dataframe
    
    Dict_Drift[FOO]=Dict_Drift[FOO].iloc[::-1]
    
    
    Time=Dict_Drift[FOO].index.view('int64')//pd.Timedelta(1,unit='s')
    Time=Time[1:]-Time[0:-1]
    Time=np.append(Time[0],Time)
    #*******And Distance****************************#
    X,Y=Lib_Ext_Cartopy.Get_Distance(Dict_Drift[FOO].lat.values,Dict_Drift[FOO].lon.values)
    
    # To get the proper size of vector and do not have derivation problem for the first and last point
    # We pad the beginning and the end with a copy of the first and last value we have, respectively
    X=np.append(np.append(X[0],X),X[-1])
    Y=np.append(np.append(Y[0],Y),Y[-1])

    #*******And now speeds**************************#
    Dict_Drift[FOO]['U-Speed'],Dict_Drift[FOO]['V-Speed'],Dict_Drift[FOO]['Time']=X/Time,Y/Time,Time
    
    #**********And now we can select data***********#
    criterion=Dict_Drift[FOO]['U-Speed'].map(lambda x : abs(x) <2.) # Creating a selection criterion
   
    # To take into account the meridional speed, we're gonna use something else
    for i in range(criterion.size):
        if abs(Dict_Drift[FOO]['V-Speed'][i])>2.:
            criterion[i]=False # We choose only the points with a meridional speed inferior to a certain threshold
    
    Dict_Drift[FOO]=Dict_Drift[FOO][criterion] #Here we apply this criterion.

# Smoothing part of the data, with a rolling mean    
Dict_Drift['Kone2']['U-Speed']=Dict_Drift['Kone2']['U-Speed'].rolling(3).mean()
Dict_Drift['Kone2']['V-Speed']=Dict_Drift['Kone2']['V-Speed'].rolling(3).mean()
Dict_Drift['Kone1']['U-Speed']=Dict_Drift['Kone1']['U-Speed'].rolling(3).mean()
Dict_Drift['Kone1']['V-Speed']=Dict_Drift['Kone1']['V-Speed'].rolling(3).mean()

# Special Data Selection due to the finite size of the region of interest. This was manually proceeded
Dict_Drift['Kone2']=Dict_Drift['Kone2'][90:-10]
Dict_Drift['Kone1']=Dict_Drift['Kone1'][:250]


#****And now if we let the music do the plotting ?

#***********Map Drawing*****************#

OSM_Image = cimgt.OSM() # Download an Open Street Map background Image
fig=plt.figure(figsize=(24,16))
# Create a GeoAxes in the tile's projection.
ax = fig.add_subplot(1, 1, 1, projection=OSM_Image.crs)

# Limit the extent of the map to a small longitude/latitude range.
ax.set_extent([164.35, 164.9, -21.14, -20.86], crs=ccrs.PlateCarree())

# Add the OSM_Image at zoom level 12.
ax.add_image(OSM_Image, 11)

# Add meridians and parallels
ax.gridlines(draw_labels=False)

   
#****Putting the data****************#

for FOO in Lib_Drift:
    Q = ax.quiver(Dict_Drift[FOO]['lon'][1:-1:3].values, Dict_Drift[FOO]['lat'][1:-1:3].values,
            Dict_Drift[FOO]['U-Speed'][1:-1:3].values,Dict_Drift[FOO]['V-Speed'][1:-1:3].values,scale=15.,
             transform=ccrs.PlateCarree(), units='width',color=Dict_color[FOO],label=FOO)

qk = ax.quiverkey(Q, 0.9, 0.9, 1., '', labelpos='E',
                  coordinates='figure') # Plot the quiver scale in the upper right of the figure


ax.legend(loc='lower right',fontsize=24)

#*****Adding a rectangle**************# 
#*****patch for the size**************#

Lib_Ext_Cartopy.Length_Patch(164.4,-21.12,Dict_Drift['Kone1']['lat'][0],ax, ccrs.PlateCarree())

#******Show and save the plot*********#
fig.show()
#fig.savefig('Kone_Lagoon_2.png',transparent=True)

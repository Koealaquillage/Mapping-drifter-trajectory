############################################"
# Library of external useful functions for #
##Cartopy                                  #
############################################

#**********Packages Import*****************#
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import cartopy.crs as ccrs

# Function to get small distances on a map
def Get_Distance(Lat,Lon):
    """Function used to get the distance between two points given in lat
    lon coordinates in meters. To get the 2 components we are going to compute 
    first as if only latitude changed and then as if longitude changed. It is
    Only to be used FOR SMALL DISTANCES. Because we are going to consider that 
    the latitude-dependant part of the formula does not change in two iterations.
    
    INPUTS:
    ------
    Lat : Numpy array of latitudes (North degrees)
    Lon : Numpy array of longitudes (East degrees)
    
    OUTPUTS:
    -------
    X : Computed Zonal distance (meters)
    Y : Computed Meridional distance (meters)
    """
    # First we need to define an useful constant
    p = np.pi/180.     #Pi/180
    rad=12742*1000 # Earth radius in meters
    #Then computing the zonal variation
    X=(np.cos((Lat[1:-1]+Lat[2:])*p/2)*(Lon[2:]-Lon[1:-1])*p)*rad
    #X=-(np.cos((Lat[1:-1]+Lat[2:])/2)*(Lon[2:]-Lon[1:-1])*p)*rad
    #And longitudinal variation
    Y= ((Lat[2:] - Lat[1:-1]) * p)*rad
    
    return X,Y

# Function to scale bar on maps for small distances
def Length_Patch(X,Y, Lat,ax,transform):
    """ Function to add a measuring length patch on a map
    so that distance are easier to realize. Need the matplotlib patch
    package.
    
    INPUTS :
    --------
    X,Y : Horizontal and vertical position of the patch on the map
    Lat : Mean Latitude of the map to compute the size of a degree
    ax : Matplotlib.ax object to be drawn on
    transform : Transformation parameter from the cartopy package
    OUTPUTS :
    --------
    ax : The modified matplotlib ax object
    """
    
    # Compute the size of a degree of longitude
    # And latitude, we do not have geoid data
    
    d_lat=110.574 # Size of a latitude degree in kilometers
    d_lon=111.320*np.cos(Lat) # Size of a longitude degree in kilometers
    
    # Size of a kilometer in degrees
    
    d_y=abs(1./d_lat)
    d_x=abs(1./d_lon)
    
    # Plotting on the ax
    #********Alternate white*************# 
    #*******and black patches************#
    for i in range(5):
        if i%2==0:
            p_lon = patches.Rectangle([X+i*abs(d_x),Y], abs(d_x), .005, color='black',transform=transform)
        else :
            p_lon = patches.Rectangle([X+i*abs(d_x),Y], abs(d_x), .005, color='white',transform=transform)
    
        ax.add_patch(p_lon)
    
    return
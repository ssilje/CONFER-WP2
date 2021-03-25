import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import cmocean as cmo
import os.path

import numpy as np
import seaborn as sns
from netCDF4 import Dataset as netcdf_dataset

import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature

def datareader(dp=[], d=[], v=[], *args):
    Dpath = []
    Dread = []
    for i in range(0,len(dp)):
        Dpath.append(dp[i] + d[i])
        if(d[i]==''):
            continue
        temp = netcdf_dataset(Dpath[i])
        try:
            Dread.append(temp.variables[v[i]][0,:,:])
        except:
            Dread.append(temp.variables[v[i]])
    try:
        Dread.append(temp.variables['lat'][:])
        Dread.append(temp.variables['lon'][:])
    except:
        print()
    return Dread
  
  
model1='chirps'
model2='ncep'
model3='dwd'
model4='ukmo'
model5='meteoFrance'
model6='ecmwf'
model7='cmcc'

season1='MAM'
season2='JJAS'
season3='OND'


#spatial plots with raw data

models = [model1,model2,model3,model4,model5,model6,model7]
seasons = [season1,season2,season3]

MOD_VAR='precip'
#OBS_VAR='precip'
#BIAS_VAR='pr'

DATAPATH = '/nird/projects/NS9853K/Teferi/data'
FIGPATH = 'plots/'

path = [DATAPATH]

variables = [MOD_VAR]

stepSize=30
colorbar_levels=np.linspace(0,18,stepSize)

for model in models:
    fig = plt.figure(figsize=(18,13))
    proj = ccrs.PlateCarree()
    ax_list = []
    gl_list = []
    ax = []
        
    for i in range(3):
        if (i == 0):
            ax_list.append(plt.subplot(1,3,i+1,projection=proj))
            gl_list.append(0)
        else:
            ax_list.append(plt.subplot(1,3,i+1, projection=proj, sharex=ax_list[0], sharey=ax_list[0]))
            gl_list.append(0)
        #print(gl_list)
            
    for i, season in zip(range(len(seasons)), seasons):
        #print(i)
        if not os.path.isfile(path[0] + MOD_VAR + '_' + model + '_' + season + '_timmean_1993-2016.nc'):  #if 'GCM-RCM' file doesn't exist, loop back
            continue
        
        data = ['precip_' + model + '_' + season + '_timmean_1993-2016.nc']
        #print(data) 
        [output, lats, lons] = datareader(path, data, variables)
              
        data_list = [output]
        labels_list = [model + '_' + season + '_1993-2016']

        CS = ax_list[i].contourf(lons, lats, data_list[0], transform=ccrs.PlateCarree(), cmap=cmo.cm.rain, extend='both')#, levels=colorbar_levels)#, norm=normalized)
        ax_list[i].coastlines()
        #ax_list[i].add_feature(shape_feature)
        ax_list[i].set(title=labels_list[0], xlabel='Longitude', ylabel='Latitude')
            
        ax_list[i].set_aspect('equal')
        
        cb = fig.colorbar(CS, ax=ax_list[i], orientation='vertical', shrink=0.4)#, format='%.2f')
        cb.set_label('Rainfall (mm/day)', fontsize=12)    
        #ax_list[i].legend(loc='upper left')
            
        gl_list[i] = ax_list[i].gridlines(crs=proj, draw_labels=True, linewidth=2, color='gray', alpha=0, linestyle='--')
        gl_list[i].top_labels = False
        gl_list[i].right_labels = False
            
        gl_list[i].xformatter = LONGITUDE_FORMATTER
        gl_list[i].yformatter = LATITUDE_FORMATTER

    plt.savefig(FIGPATH + 'precip_' + model + '_all_seasons_raw_1993-2016' + '.png', format='png', dpi=250, bbox_inches='tight')
    

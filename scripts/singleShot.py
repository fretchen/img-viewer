
'''
A simple script for plotting up an overview of a shot.
'''

# general
import lyse as ly
import h5py
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from mpl_toolkits.axes_grid1 import make_axes_locatable

#get the images
r = ly.Run(ly.path, no_write = True);
with h5py.File(r.h5_path) as h5_file:
    run_nr = int(h5_file.attrs['run number']);
    Fig_Title = r.h5_path#h5_file.filename


png_name1=Fig_Title[:Fig_Title.rindex('\\')+1]
png_name1=png_name1[:-1]
png_name1=png_name1[:png_name1.rindex('\\')+1]
png_name1=png_name1+"Images"
png_name2=Fig_Title[Fig_Title.rindex('\\'):]
png_name2=png_name2[:-3]+".png"
png_name=png_name1+png_name2

Note=r.get_globals()['Summary']
Fig_Title=Fig_Title+"\n"+Note

orientation = 'mako';
name = 'frame';

Iat = r.get_image(orientation,'fake3',name);
Iref = r.get_image(orientation,'fake4',name);
Ibg = 0.0*Iat

Iat = 1.0 *Iat
Iref = 1.0 *Iref

Iat = Iat-Ibg
Iref = Iref-Ibg

left=0 #min value 0
right=644 #max value 644 for Mako
up=200 #min value 0
down=450 #max value 484 for Mako


od =Iat-Iref

odx = np.sum(od, axis=0)
ody = np.sum(od, axis=1)

back=r.get_image(orientation,'fake1',name);
fluo=r.get_image(orientation,'fake2',name);
subtracted=(1.0*fluo)-(1.0*back)

fig, (ax1, ax2) = plt.subplots(1, 2,figsize=(15,10), gridspec_kw={'width_ratios': [10, 2]})#fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
fig.suptitle(Fig_Title)

#########################################
ax1.set_title('Fluorescence Image',loc='left')
ax1.axis('off')
ax2.set_title('MOT')
ax2.tick_params(direction='in')
img1=ax1.imshow(od, cmap='Oranges',vmin=0, vmax=4)
fig.colorbar(img1,ax=ax1,shrink=0.6, pad=0.01)
divider = make_axes_locatable(ax1)
axbottom = divider.append_axes("bottom", size=1, pad=0.2, sharex=ax2)
axleft = divider.append_axes("left", size=1, pad=0.2, sharey=ax2)
axleft.invert_xaxis()
axbottom.plot(np.arange(len(odx)), odx,'-g')
axbottom.tick_params(direction='in')
axleft.plot(ody, np.arange(len(ody)),'-g')
axleft.tick_params(direction='in')
axbottom.margins(x=0)
axleft.margins(y=0)
img2=ax2.imshow(subtracted, cmap='Oranges',vmin=0, vmax=80)
fig.colorbar(img2, ax=ax2,shrink=0.2)
fig.tight_layout()

fig.savefig(png_name, bbox_inches='tight')

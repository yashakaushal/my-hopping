#!/usr/bin/env python
# coding: utf-8

# In[265]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#from mpl_toolkits.basemap import Basemap
#import ephem # to make coordinate systems conversions
from IPython.core.display import HTML # To include images as HTML
import requests
from bs4 import BeautifulSoup


# In[303]:


cd /Users/yashakaushal/Documents/summer_project/


# In[304]:


#reading catalog and dropping nan values
star_cat = pd.read_csv("/Users/yashakaushal/Documents/summer_project/data_webscraping.csv")
star_cat = star_cat.dropna(subset=["spect","mag"])

#reading columns
ra = star_cat["rarad"]
dec = star_cat["decrad"]
spect = star_cat["spect"]
mag = star_cat["mag"]
flux = 10**(-mag/2.5)

#defining spectral cuts
omask = spect.str.startswith('O')
bmask = spect.str.startswith('B')
fmask = spect.str.startswith('F')
mmask = spect.str.startswith('M')

#variable star cat
var_star = star_cat[["rarad","decrad","var_min","var_max",]]
var_star = var_star.dropna()


# In[47]:


def plot_mwd(RA,Dec,org=0,title='Mollweide projection', projection='mollweide'):
    ''' RA, Dec are arrays of the same length.
    RA takes values in [0,360), Dec in [-90,90],
    which represent angles in degrees.
    org is the origin of the plot, 0 or a multiple of 30 degrees in [0,360).
    title is the title of the figure.
    projection is the kind of projection: 'mollweide', 'aitoff', 'hammer', 'lambert'
    '''
    x = np.remainder(RA+360-org,360) # shift RA values
    ind = x>180
    x[ind] -= 360    # scale conversion to [-180, 180]
    x = -x    # reverse the scale: East to the left
    tick_labels = np.array([150, 120, 90, 60, 30, 0, 330, 300, 270, 240, 210])
    tick_labels = np.remainder(tick_labels+360+org,360)
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(111, projection=projection, facecolor ='black',alpha=0.5)
    ax.scatter(np.radians(x),np.radians(Dec))  # convert degrees to radians
    ax.set_xticklabels(tick_labels)     # we add the scale on the x axis
    ax.set_title(title)
    ax.title.set_fontsize(15)
    ax.set_xlabel("RA")
    ax.xaxis.label.set_fontsize(12)
    ax.set_ylabel("Dec")
    ax.yaxis.label.set_fontsize(12)
    ax.grid(True)


# In[306]:


plt.rcParams["figure.figsize"]=(20,12)
f=15

plt.subplot(221, projection="mollweide", facecolor='grey')
plt.scatter(ra[omask],dec[omask], s=1e3*flux[omask], color='blue')
plt.title("O-type stars", fontsize=f)
plt.grid(True)

plt.subplot(222, projection="mollweide", facecolor='grey')
plt.scatter(ra[bmask],dec[bmask], s=1e2*flux[bmask], color='blue')
plt.title("B-type stars", fontsize=f)
plt.grid(True)

plt.subplot(223, projection="mollweide", facecolor='grey')
plt.scatter(ra[fmask],dec[fmask], s=1e2*flux[fmask], color='blue')
plt.title("F-type stars",fontsize=f)
plt.grid(True)

plt.subplot(224, projection="mollweide", facecolor='grey')
plt.scatter(ra[mmask],dec[mmask], s=1e2*flux[mmask], color='blue')
plt.title("M-type stars",fontsize=f)
plt.grid(True)

plt.savefig("Ans_1")
plt.show()

# In[246]:

page = requests.get("http://astrosat.iucaa.in/czti/?q=grb")
soup = BeautifulSoup(page.content, 'lxml')
tab = soup.find_all('table')[0]
tab

data = [[]]
for i in tab.find_all('tr'):   #searching in each row of the table ( 'tr' tag stands for row)
    row = []                    #declaring empty row
    for j in i.find_all('td'):  #'td' tag stands for a cell
        row.append(j.get_text().strip('\n').strip('\t'))   #add the text contents of each row to the list
    data.append(row)
    
# hack to fix the radec values with no commas
data[163][3] = '61.680, -2.606'
data[178][3] = '238.044, +70.142 '


# In[261]:


df = pd.DataFrame(index=np.arange(len(data)-2),columns=['No','Name','Ra_deg','Dec_deg'])

for i in range(len(data)-2):
    if (data[i+2][3]=='--'):
        pass
    else:
        df['No'].iloc[i] = data[i+2][0]
        df['Name'].iloc[i] = data[i+2][1]
        df['Ra_deg'].iloc[i] = data[i+2][3].split(',')[0]
        df['Dec_deg'].iloc[i] = data[i+2][3].split(',')[1]
        
df = df.dropna()
df = df.drop(18) #non integer value
df[["Ra_deg","Dec_deg"]] = df[["Ra_deg","Dec_deg"]].astype(float) #convert Ra Dec to numeric values


# In[307]:


plt.rcParams["figure.figsize"]=(20,12)
f=15

plt.subplot(111,projection="mollweide", facecolor='gray',alpha=0.1)
plt.scatter(ra,dec, s=300*flux, color='aqua',label="All stars")
plt.scatter(np.radians(df["Ra_deg"]), np.radians(df["Dec_deg"]), color='blue',zorder=1,label="GRBs")
plt.scatter(var_star["rarad"], var_star["decrad"], color= 'yellow',zorder=0, label="Variable Star")
plt.title("All stars", fontsize=20)
plt.legend(fontsize=15)
plt.grid(True)
plt.savefig("Ans_2")


# In[308]:


get_ipython().system('jupyter nbconvert --to script summer_proj.ipynb')


# In[ ]:





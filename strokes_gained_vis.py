# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 13:58:14 2018

@author: c560396
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def discrete_cmap(N, base_cmap=None):
    """Create an N-bin discrete colormap from the specified input map"""

    # Note that if base_cmap is a string or None, you can simply do
    #    return plt.cm.get_cmap(base_cmap, N)
    # The following works for string, None, or a colormap instance:

    base = plt.cm.get_cmap(base_cmap)
    color_list = base(np.linspace(0, 1, N))
    cmap_name = base.name + str(N)
    return base.from_list(cmap_name, color_list, N)




# define the data
cols = ['Stroke','Club','Phase','Start Loc','Start Dist', 'End Loc', 'End Dist', 'Strokes Gained', 
        'Tee', 'Course', 'Date', 'Strokes to Hole']

data = pd.read_csv('rounds\\Taillie_History.csv', header = 0, usecols = cols )
clubs = {'Driver':0, '3W' :1, '3H' :2, '4i':3, '5i':4, '6i' :5, '7i':6, '8i':7,'9i':8, 'PW':9, 'AW':10,'SW':11, 'LW':12,'Putter':13, 'Penalty':14}


#plot all data

fig, ax = plt.subplots()

fig = plt.scatter(data['Start Dist'], data['Strokes Gained'], c = data['Club'].apply(lambda x: clubs[x]), s=50,
            cmap = discrete_cmap(len(clubs), 'Spectral'))
cbar = plt.colorbar(ticks = range(len(clubs)), orientation = 'vertical')
plt.clim(-0.5, len(clubs)-0.5)
cbar.ax.set_yticklabels(['Driver', '3W', '3H','4i','5i','6i','7i','8i','9i','PW','AW','SW','LW','Putter', 'Penalty'])

plt.grid(True)
plt.suptitle('Strokes Gained vs Distance')
plt.xlabel('Distance from Hole')
plt.ylabel('Strokes Gained')

#plot all data no putting
fig3, ax3 = plt.subplots()
data_sub = data.where(data["Phase"] != "Green")
data_sub = data_sub.dropna(how ='any')
fig = plt.scatter(data_sub['Start Dist'], data_sub['Strokes Gained'], c = data_sub['Club'].apply(lambda x: clubs[x]), s=50,
            cmap = discrete_cmap(len(clubs), 'Spectral'))
cbar = plt.colorbar(ticks = range(len(clubs)), orientation = 'vertical')
plt.clim(-0.5, len(clubs)-0.5)
cbar.ax.set_yticklabels(['Driver', '3W', '3H','4i','5i','6i','7i','8i','9i','PW','AW','SW','LW','Putter', 'Penalty'])
plt.suptitle('Strokes Gained Tee to Green')
plt.xlabel('Distance from Hole (YDS)')
plt.ylabel('Strokes Gained')
plt.grid(True)



#plot putting only
fig2, ax2 = plt.subplots()
data_putting = data.where(data["Phase"] == "Green")
data_putting = data_putting.dropna(how = 'any')
plt.scatter(data_putting["Start Dist"], data_putting["Strokes Gained"])
plt.grid(True)
plt.suptitle('Strokes Gained Putting')
plt.xlabel('Distance from Hole')
plt.ylabel('Strokes Gained')
plt.grid(True)

#loop for all stages
types = ['Tee', 'APPR210+','APPR176-210','APPR125-175','APPR<125', 'Short Game','Green', 'Recovery']
for value in types:
    plt.figure()
    subs = data.where(data["Phase"] == value)
    subs = subs.dropna(how = 'any')
    plt.scatter(subs["Start Dist"], subs["Strokes Gained"], c = subs['Club'].apply(lambda x: clubs[x]), s=50,
            cmap = discrete_cmap(len(clubs), 'Spectral'))
    cbar = plt.colorbar(ticks = range(len(clubs)), orientation = 'vertical')
    plt.clim(-0.5, len(clubs)-0.5)
    a = subs["Club"].unique().tolist()
    a.sort()
    cbar.ax.set_yticklabels(['Driver', '3W', '3H','4i','5i','6i','7i','8i','9i','PW','AW','SW','LW','Putter', 'Penalty'])
    plt.suptitle('Strokes Gained ' + value)
    plt.xlabel('Distance from Hole (YDS)')
    plt.ylabel('Strokes Gained ' + value)
    plt.grid(True)
    
#stats for each round
plt.figure()
for value in data["Date"].unique().tolist():
    sub = data.where(data["Date"] == value)
    sub = sub.dropna(how = 'any')
    sums = []
    for item in types:
        a = sub["Strokes Gained"][sub["Phase"]==item].sum()
        sums.append(a)
    plt.plot(types, sums, '*', label = value)
plt.suptitle('Round Summaries')
plt.legend()


#round progression
plt.figure()
sub2 = data.where(data["Date"] == '12/14/2018')
sub2 = sub2.dropna(how = 'any')
sub2 = sub2.reset_index()
plt.plot(sub2["Start Dist"], 'o')


#plot vs baseline putting
putt_subs = data.where(data["Phase"] == 'Green')
putt_subs = putt_subs.dropna(how = 'any')
a = putt_subs["Start Dist"].unique().tolist()
a.sort()
av = []
for value in a:
    putt_sub2 = putt_subs.where(putt_subs["Start Dist"] == value)
    av.append(putt_sub2["Strokes to Hole"].mean())
bsln = pd.read_csv('data\\green.txt', header = 0, delimiter = '\t', names = ['Strokes'])
plt.plot(bsln.index, bsln["Strokes"], 'k-', label = 'PGA Baseline')
plt.scatter(a, av, c = 'g', label = 'D. Taillie')
plt.grid()
plt.legend()
plt.suptitle('D. Taillie Putting Average vs PGA Tour')
plt.xlabel('Feet from Hole')
plt.ylabel('Average No. of Putts')

#plot vs baseline fairway
putt_subs = data.where(data["Start Loc"] == 'Fairway')
putt_subs = putt_subs.dropna(how = 'any')
a = putt_subs["Start Dist"].unique().tolist()
a.sort()
av = []
for value in a:
    putt_sub2 = putt_subs.where(putt_subs["Start Dist"] == value)
    av.append(putt_sub2["Strokes to Hole"].mean())
bsln = pd.read_csv('data\\fairway.txt', header = 0, delimiter = ',', names = ['Strokes'])
plt.plot(bsln.index, bsln["Strokes"], 'k-', label = 'PGA Baseline Fairway')
plt.scatter(a, av, c = 'g', label = 'D. Taillie')
plt.grid()
plt.legend()
plt.suptitle('D. Taillie Fairway Average vs PGA Tour')
plt.xlabel('Dist from Hole')
plt.ylabel('Shots til Holed')




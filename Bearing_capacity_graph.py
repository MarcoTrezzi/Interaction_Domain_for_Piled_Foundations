import pandas as pd
import os
import matplotlib.pyplot as plt
from IPython.display import display

path = os.getcwd()
path_bearing_capacity = os.path.join(path,'Bc.xlsx') #PERCORSO FILE FOGLIO CALCOLO
nome = str('Bc_graph')

df = pd.read_excel(nome + str('.xlsx'), sheet_name='Foglio1')

lmax = 40

df_0 = df[['Lpalo', 'R3cLT', 'R3tLT']]
df_graph = df_0[df_0['Lpalo'] <= lmax]
display(df_graph)

rcd = df_graph['R3cLT']
rtd = df_graph['R3tLT']
length = df_graph['Lpalo']

x_max_graph = round(max(rcd), -3)
y_max_graph = round(max(length))

fig, ax = plt.subplots(figsize=(7,10))
fig.suptitle('Bearing capacity - D=800 [mm]')
ax.plot(rcd, length, label = 'Rd - Compression')
ax.plot(rtd, length, label = 'Rd - Tension')

ax.set_xlim([0, max(rcd) * 1.1])
ax.set_ylim([0, lmax])
ax.set_xlabel('Rd [kN]')
ax.set_ylabel('Pile length [m]')

ax.xaxis.set_label_position('top')
ax.xaxis.tick_top()
ax.legend ()
ax.invert_yaxis()


plt.tick_params(axis='x', direction='in')
plt.tick_params(axis='y', direction='in')

plt.grid()


fig.tight_layout()
plt.savefig(str('D=800 [mm]'), format="png")
plt.show()



import pandas as pd
import os
import matplotlib.pyplot as plt
import math
from IPython.display import display

path = os.getcwd()
path_bearing_capacity = os.path.join(path,'Results.xlsx') #PERCORSO FILE FOGLIO CALCOLO
nome = str('Results')

df = pd.read_excel(nome + str('.xlsx'), sheet_name='Results')

lmax = max(df['Lpile [m] outermost'])

df['Mtot [kNm]'] = round((df['Mx [kNm]']**2 + df['My [kNm]']**2)**(1/2),0)
df['%saving'] = round(df['%length'],2)*100


display(df)

df_45 = df[df['alfa [°]']==45]
df_00 = df[df['alfa [°]']==90]

print(df_00)

salv_45 = df_45['%saving']
mtot_45 = df_45['Mtot [kNm]']

salv_00 = df_00['%saving']
mtot_00 = df_00['Mtot [kNm]']


#x_max_graph = round(max(rcd), -3)
#y_max_graph = round(max(length))

fig, ax = plt.subplots(figsize=(7,10))
fig.suptitle('Saving percentage')
ax.plot(salv_45, mtot_45, label = 'alfa = 45°')
ax.plot(salv_00, mtot_00, label = 'alfa = 0°')

ax.set_xlim([0, max(salv_45) * 1.1])
ax.set_ylim([0, max(mtot_45)])
ax.set_xlabel('Saving percentage [%]')
ax.set_ylabel('Mtot [kNm]')

ax.xaxis.set_label_position('top')
ax.xaxis.tick_top()
ax.legend ()
ax.invert_yaxis()

plt.tick_params(axis='x', direction='in')
plt.tick_params(axis='y', direction='in')

plt.grid()


fig.tight_layout()
plt.savefig(str('D=1000 [mm]'), format="png")
plt.show()



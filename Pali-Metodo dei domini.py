import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

path = os.getcwd()
# LEGGERE CARATTERISTICHE GEOMTERICHE PALIFICATA E COMBINAZIONI DI CARICO
df_palificata = pd.read_csv('Dati_palificata.csv', delimiter=',')
df_carichi = pd.read_csv('Combinazioni_carico.csv', delimiter=',')

# CREO ARRAY CON VALORI DI ALFA PER IL CALCOLO DEL DOMINIO
alfa_calc = np.array(list(set(df_carichi['alfa [°]'])))

coord_x = df_palificata['X [m]']
coord_y = df_palificata['Y [m]']

# DEFINIRE FUNZIONE PER CALCOLARE GLI PSI ED ETA DI OGNI PALO
def calc_psi (alpha_coo,xj,yj):
    psi_j = xj * np.cos(np.radians(alpha_coo)) - yj * np.sin(np.radians(alpha_coo))
    return psi_j

nomi_domini = []
res_nu = []
res_mu = []

#CALCOLO DOMINIO PER TUTTI GLI ALFA
for alfa in alfa_calc:
    psi_calc = []
    Nu = []
    Mu = []

    df_palificata_calc = df_palificata                                          #DATAFRAME TEMPORANEO PER ITERAZIONE
    nomi_domini.append("alfa = " + str(alfa))
    for xj_calc, yj_calc in zip(coord_x, coord_y):                              #ITERO PER CALCOLARE PSI ED ETA DI OGNI PALO
        psi_calc.append(round(calc_psi(alfa, xj_calc, yj_calc),2))              #CREO ARRAY COORD PSI
    np_psi_calc = np.array(psi_calc)

    df_pal_tot = df_palificata_calc.assign(psi = np_psi_calc)                   #AGGIUNGO LA COLONNA CON PSI AL DATAFRAME, MA CREANDONE UNO NUOVO
    df_pal_tot['psi_c'] = (df_pal_tot['Rcd [kN]'] * df_pal_tot['psi'])
    df_pal_tot['psi_t'] = (df_pal_tot['Rtd [kN]'] * df_pal_tot['psi'])

    sorted_df_pal_tot = df_pal_tot.sort_values(['psi'], ascending = True)       #SORT DEL DATAFRAME CON PSI CRESCENTE

    rcd_somm = sorted_df_pal_tot['Rcd [kN]']
    rtd_somm = sorted_df_pal_tot['Rtd [kN]']
    rcd_psi_somm = sorted_df_pal_tot['psi_t']
    rtd_psi_somm = sorted_df_pal_tot['psi_t']
                                                                                # CREARE NOMI DEGLI ARRAY NUMPY PER PLOT DOMINIO                                                                                    # CREARE ARRAY NUMPY SALVATO CON IL NOME DELL'ALFA PER PLOTTARLI TUTTI ALLA FINE
    for i in df_palificata['Numero_palo']:
        print(i)
        if i==1:
            Nu.append(round(sum(sorted_df_pal_tot['Rtd [kN]'] * -1), 2))
            Mu.append(sum(rtd_psi_somm[i-1:]))
        else:
            Nu.append(sum(rcd_somm[: i-1]) - sum(rtd_somm[i-1 :]))
            Mu.append(sum(- rcd_psi_somm[: i-1]) + sum(rtd_psi_somm[i-1:]))
            
    for k in df_palificata['Numero_palo']:
        print(k)
        if k==1:
            Nu.append(round(sum(sorted_df_pal_tot['Rcd [kN]']), 2))
            Mu.append(- sum(rtd_psi_somm[k-1:]))
        else:
            Nu.append(sum(rcd_somm[k-1:]) - sum(rtd_somm[:k-1]))
            Mu.append(sum(rcd_psi_somm[: k-1]) - sum(rtd_psi_somm[k-1:]))

        #CHIUSURA DOMINIO
    n_ini = Nu[0]
    m_ini = Mu[0]
    Nu.append(n_ini)
    Mu.append(m_ini)

    res_nu.append(Nu)
    res_mu.append(Mu)

fig, ax = plt.subplots()

for alpha_leg, nu, mu in zip(alfa_calc, res_nu, res_mu):
    ax.plot(nu,mu, label = 'alfa=' + str(alpha_leg), marker = 'o')
    carichi_plot = df_carichi[df_carichi['alfa [°]'] == alpha_leg]
    ax.scatter(carichi_plot['Ned [kN]'], carichi_plot['Medtot [kNm]'])
    print(carichi_plot['Ned [kN]'])
    print(carichi_plot['Medtot [kNm]'])


ax.set_xlabel('N [kN]')
ax.set_ylabel('M [kN]')
ax.legend()

plt.grid()
fig.tight_layout()
plt.show()

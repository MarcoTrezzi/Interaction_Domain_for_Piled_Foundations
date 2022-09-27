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

print(df_palificata)
print(df_carichi)
print(alfa_calc)

coord_x = df_palificata['X [m]']
coord_y = df_palificata['Y [m]']

# DEFINIRE FUNZIONE PER CALCOLARE GLI PSI ED ETA DI OGNI PALO
def calc_psi (alpha_coo,xj,yj):
    psi_j = xj * np.cos(np.radians(alpha_coo)) - yj * np.sin(np.radians(alpha_coo))
    return psi_j

def calc_eta (alpha_coo, xj, yj):
    eta_j = xj * np.sin(np.radians(alpha_coo)) - yj * np.cos(np.radians(alpha_coo))
    return eta_j


nomi_domini = []
psi_calc = []
eta_calc = []


#CALCOLO DOMINIO PER TUTTI GLI ALFA
for alfa in alfa_calc:

    df_palificata_calc = df_palificata                              #DATAFRAME TEMPORANEO PER ITERAZIONE
    nomi_domini.append("alfa = " + str(alfa))
    for xj_calc, yj_calc in zip(coord_x, coord_y):                  #ITERO PER CALCOLARE PSI ED ETA DI OGNI PALO
        psi_calc.append(round(calc_psi(alfa, xj_calc, yj_calc),2))  #CREO ARRAY COORD PSI
        eta_calc.append(round(calc_eta(alfa, xj_calc, yj_calc),2))  #CREO ARRAY COORD ETA
    np_psi_calc = np.array(psi_calc)
    np_eta_calc = np.array(eta_calc)

    df_pal_tot = df_palificata_calc.assign(psi = np_psi_calc, eta = np_eta_calc)       #AGGIUNGO LE COLONNE CON PSI ED ETA AL DATAFRAME, MA CREANDONE UNO NUOVO
    df_pal_tot['psi_c'] = (df_pal_tot['Rcd [kN]'] * df_pal_tot['psi'])
    df_pal_tot['psi_t'] = (df_pal_tot['Rtd [kN]'] * df_pal_tot['psi'])


    psi_calc.clear()                                                                   #SVUOTO GLI ARRAY  CON PSI ED ETA PER LA PROSSIMA ITERAZIONE
    eta_calc.clear()
    print (df_pal_tot)
    sorted_df_pal_tot = df_pal_tot.sort_values(['psi'], ascending = True)              #SORT DEL DATAFRAME CON PSI CRESCENTE
    print (sorted_df_pal_tot)

    rcd_somm = sorted_df_pal_tot['Rcd [kN]']
    rtd_somm = sorted_df_pal_tot['Rtd [kN]']
    rcd_psi_somm = sorted_df_pal_tot['psi_t']
    rtd_psi_somm = sorted_df_pal_tot['psi_t']

    Nu = []
    Mu = []                                                                                       # CREARE NOMI DEGLI ARRAY NUMPY PER PLOT DOMINIO                                                                                    # CREARE ARRAY NUMPY SALVATO CON IL NOME DELL'ALFA PER PLOTTARLI TUTTI ALLA FINE
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

    #plt.plot(Nu,Mu, marker = 'o')

print(psi_calc)
print(eta_calc)
print (Nu)
print (Mu)

plt.plot(Nu,Mu, marker = 'o')
plt.show()
print(alfa_calc)
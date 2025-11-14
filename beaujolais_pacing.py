import numpy as np
import scipy
import matplotlib.pyplot as plt

############################################
############# RACE PARAMETERS ##############
############################################

ravito_coordinnates = np.array([4,10,15,16.5,17.5,21.1,24,27,30.1,34,37,39,41,42.195])# [km]
N_ravito = len(ravito_coordinnates) # Number of enjoyed ravitos
T_ravito = 5 # mean time spent per ravito [min]
V_ravito = 60 # mean consumption (degustation) per ravition [mL]
bw = 80 #body weight


###############################################
########### MODELLING RACE OUTCOME ############
###############################################

X = np.linspace(0,42,421) # Distance covered

def elapsed_time(list_v):
    res_T = [0]
    for i in range(1,len(X)):
        dX = X[i] - X[i-1]
        dT = dX * list_v[i]
        if X[i] in ravito_coordinnates:
            dT += T_ravito
        res_T.append(res_T[-1] + dT)
    return np.array(res_T)

def alcoolemie(t, V):
    b = 1/30
    a = b * np.exp(1) * V * 0.12 * 0.8 / (0.7 * bw)
    return float(a * t * np.exp(-b * t))

def effect_one_ravito(t_ravito, time, V):
    return np.array([alcoolemie(t-t_ravito, V) if t >= t_ravito else 0 for t in time])

#def alcohol_level(ravito_coordinnates, V_ravito):
#    res_C = np.zeros(X.shape)
#    running_time = elapsed_time(list_v)
#    for i, coord in enumerate(ravito_coordinnates):
#        t_ravito = running_time[X == coord]
#        res_C = res_C + effect_one_ravito(t_ravito, running_time, V_ravito)
#        #plt.plot(running_time, effect_one_ravito(t_ravito, running_time, V_ravito))
#    return res_C

def alcohol_level(ravito_coordinnates, list_v, V_ravito):
    res_C = np.zeros(X.shape)
    running_time = elapsed_time(list_v)
    t_ref = 0
    res_C_ref = 0
    for i, t_i in enumerate(running_time):
        if X[i] in ravito_coordinnates: # reset alcohol computation with new offset at each ravito
            t_ref = t_i
            res_C_ref = res_C[i-1]
        res_C[i] = alcoolemie(t_i-t_ref, V_ravito)+res_C_ref
    return res_C

    
def plot_pacing(list_v, name="pacing_plan"):
    fig, axs = plt.subplots(2,2, figsize = (15,12))

    #axs[0,0].scatter(ravito_coordinnates, [4] + list(ravito_coordinnates[1:]-ravito_coordinnates[:-1]))
    axs[0,0].stem(np.arange(len(ravito_coordinnates)), [4] + list(ravito_coordinnates[1:]-ravito_coordinnates[:-1]))
    axs[0,0].set_ylabel("Distance inter-ravito (km)", fontsize='large')
    axs[0,0].set_ylim([0,7])

    axs[0,1].plot(X, list_v)
    axs[0,1].axhline(np.mean(list_v), color='k', ls='--', alpha=1)
    axs[0,1].text(0.5,np.mean(list_v)+0.02, f"Moy : {np.round(np.mean(list_v),2)}  min/km", color='k')
    axs[0,1].set_ylabel("Allure (min/km)", fontsize='large')
    axs[0,1].set_xlim([0,ravito_coordinnates[-1]])
    for d in [10,21.1,30]:
        axs[0,1].axvline(d, color='k', ls='--', alpha=0.3)
        axs[0,1].text(d-1, list_v[-1],f"{d} km", alpha=0.8,)
        
    time = elapsed_time(list_v)/60
    axs[1,0].plot(X, time)       
    axs[1,0].set_ylabel("Temps écoulé (h)", fontsize='large')
    axs[1,0].text(X[-1]-4, np.round(time[-1],2)+0.1, f"Temps final\n{np.round(time[-1],2)} h",)
    axs[1,0].set_ylim([0,5.99])
    axs[1,0].set_xlim([0,ravito_coordinnates[-1]])
    for d in [10,21.1,30]:
        axs[1,0].axvline(d, color='k', ls='--', alpha=0.3)
        #axs[1,0].axhline(time[X==d], color='k', ls='--', alpha=0.3)
        axs[1,0].text(d-2.5, time[X==d]+0.05, f"{np.round(time[X==d],2)[0]} h" , color='k', alpha=1)
        axs[1,0].text(d-1, 1.1*time[-1], f"{d} km", alpha=0.8,)
        
    alcohol = alcohol_level(ravito_coordinnates, list_v, V_ravito)
    axs[1,1].plot(X, alcohol)
    axs[1,1].text(X[-1]-4, np.round(alcohol[-1],2)+0.02, f"Murge finale\n{np.round(alcohol[-1],2)} g/L",)
    axs[1,1].axhline(0.5, color='k', ls='--', alpha=1)
    axs[1,1].set_ylabel("Alcoolémie (g/L)", fontsize='large')
    axs[1,1].fill_between(X[alcohol>0.5], 0.5, alcohol[alcohol>0.5], color='r', alpha=0.3)
    axs[1,1].text(30, 0.6, 'No car zone', color='r', fontsize='large')
    #axs[1,1].set_ylim([0,3])
    axs[1,1].set_xlim([0,ravito_coordinnates[-1]])
    for d in [10,21.1,30]:
        axs[1,1].axvline(d, color='k', ls='--', alpha=0.3)
        axs[1,1].text(d-2.5, alcohol[X==d]+0.05, f"{np.round(alcohol[X==d],2)[0]} g/L" , color='k', alpha=1)
        axs[1,1].text(d-1, alcohol[-1],f"{d} km", alpha=0.8,)

    axs[0,0].set_xlabel("Numéro ravito", fontsize='large')
    axs[0,1].set_xlabel("Distance parcourue (ravitos)", fontsize='large')
    axs[1,0].set_xlabel("Distance parcourue (ravitos)", fontsize='large')
    axs[1,1].set_xlabel("Distance parcourue (ravitos)", fontsize='large')

    axs[0,0].set_xticks(np.arange(len(ravito_coordinnates)))
    axs[0,1].set_xticks(ravito_coordinnates, [f"{k}" for k in range(1,len(ravito_coordinnates)+1)])
    axs[1,0].set_xticks(ravito_coordinnates, [f"{k}" for k in range(1,len(ravito_coordinnates)+1)])
    axs[1,1].set_xticks(ravito_coordinnates, [f"{k}" for k in range(1,len(ravito_coordinnates)+1)])
    
    for i in range(2):
        for j in range(2):
            axs[i,j].spines[["top","right"]].set_visible(False)
    
    fig.tight_layout()
    axs[0,1].set_title(name,fontsize='xx-large')
    plt.savefig(name+'.png', dpi=300)

###############################################
################# STRATEGY 1 ##################
####### Positive split after each ravito ######
###############################################
v_0 = 5.25 # initial pace [min/km]
v_i = v_0
list_v = []
for i, X_i in enumerate(X):
    if X_i in ravito_coordinnates:
        v_i += 0.1
    list_v.append(v_i)
list_v = np.array(list_v)

plot_pacing(list_v, "positive_split")


###############################################
################# STRATEGY 2 ##################
####### Negative split after each ravito ######
###############################################
v_0 = 6.3 # initial pace [min/km]
v_i = v_0
list_v = []
for i, X_i in enumerate(X):
    if X_i in ravito_coordinnates:
        v_i -= 0.1
    list_v.append(v_i)
list_v = np.array(list_v)

plot_pacing(list_v, "negative_split")


###############################################
################# STRATEGY 3 ##################
# Running pace depends on gap between ravitos #
###############################################
v_0 = 5.5
v_i = v_0
list_v = []

def vitesse(distance):
    return float((distance-1)/3+4.5)

ravito_coordinnates_extended = [0]+ravito_coordinnates
for i, X_i in enumerate(X):
    if X_i in ravito_coordinnates_extended:
        X_next_rav =  ravito_coordinnates_extended[np.where(ravito_coordinnates_extended==X_i)[0]+1]
        v_i = vitesse(X_next_rav-X_i)
    list_v.append(v_i)
list_v = np.array(list_v)
plot_pacing(list_v, "quand_le_prochain_ravito_est_proche_on_accelere")


################################################
################## STRATEGY 4 ##################
## Running pace depends on gap between ravitos #
################################################
#v_0 = 5.5
#v_i = v_0
#list_v = []
#
#def vitesse(distance):
#    return float(-0.4*distance +7.4)
#
#ravito_coordinnates_extended = [0]+ravito_coordinnates
#for i, X_i in enumerate(X):
#    if X_i in ravito_coordinnates_extended:
#        X_next_rav =  ravito_coordinnates_extended[np.where(ravito_coordinnates_extended==X_i)[0]+1]
#        v_i = vitesse(X_next_rav-X_i)
#    list_v.append(v_i)
#list_v = np.array(list_v)
#plot_pacing(list_v)
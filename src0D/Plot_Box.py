import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd 
from matplotlib.lines import Line2D
import seaborn as sns


Reduced  = pd.read_csv("./Mech_Input/Change/Err_Absolute.csv")
Smoke_gen1 = pd.read_csv("./Mech_OptiSmoke_2/Change_Gen1/Err_Absolute.csv")
Smoke_gen200= pd.read_csv("./Mech_OptiSmoke_2/Change_Gen500/Err_Absolute.csv")
MechOpt_gen1 = pd.read_csv("./Mech_PyOptMech_2/Change_Gen1/Err_Absolute.csv")
MechOpt_gen200= pd.read_csv("./Mech_PyOptMech_2/Change_Gen500/Err_Absolute.csv")


species_of_interest = ["H2", "NH3","H2O","N2O","NO","NO2"]
# species_of_interest = ["H2", "NH3","H2O","NO","NO2"]
list_spec = ["Y_" + col for col in species_of_interest]

positions = np.arange(len(list_spec))[:, None] * 5 + np.arange(0, 5, 1)
position1, position2, position3, position4, position5 = positions.T

colors = ['yellow', '#FF9999', '#FF0000', '#9999FF', '#0000FF']   # Define colors for each dataset
datasets = [Reduced, Smoke_gen1, MechOpt_gen1, Smoke_gen200, MechOpt_gen200]
labels = ['Reduced', 'Smoke Gen1', 'MechOpt Gen1', 'Smoke Gen500', 'MechOpt Gen500']

positions = [position1, position2, position3, position4, position5]

for data, pos, color in zip(datasets, positions, colors):
    plt.boxplot(data[list_spec], positions=pos, patch_artist=True, 
                labels=list_spec, showfliers=False, 
                boxprops=dict(facecolor=color, color=color), 
                medianprops=dict(color='black'))  # Médiane en noir pour visibilité


for i in range(0, len(position5)):
    plt.axvline(x=position5[i]+0.5, color='black', linestyle='--', linewidth=1)

plt.xticks(position3-0.5, list_spec)  # Ajuste les étiquettes pour les positions

legend_handles = [Line2D([0], [0], color=color, lw=4, label=label) for color, label in zip(colors, labels)]

# Add legend
plt.legend(handles=legend_handles, loc="best")

plt.savefig("Boxplot.png")
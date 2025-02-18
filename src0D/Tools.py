import numpy as np 
import numpy as np 
import pandas as pd 
import glob
import os 
import re 
from scipy.interpolate import interp1d

class MinMaxScaler:
    def fit(self, x):
        self.min = x.min(0)
        self.max = x.max(0)

    def transform(self, x):
        x = (x - self.min) / (self.max - self.min + 1e-7)
        return x

    def inverse_transform(self, x):
        x = self.min + x * (self.max - self.min + 1e-7)
        return x
    
def ai_delay(data,alpha =0.05):
    time=data["t"]
    Temperature=data["T"]
    T_init = Temperature[0]
    T_max = max(Temperature)
    
    ignition_temp = T_init + alpha * (T_max - T_init)
    
    for i, T in enumerate(Temperature):
        if T >= ignition_temp:
            return time[i]
        
def interp(data_grid : list,data_value : dict,commun_grid : list ):
    
    int_func = interp1d(data_grid, data_value, fill_value="extrapolate")
    output = int_func(commun_grid)
    return output


    
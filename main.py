import os
from os import path
from modules.physics import *
from modules.plots import *
from modules.analyse import *
from modules.analyse import *
import pandas as pd

if __name__ == '__main__':
    proton_range_data =\
        pd.read_csv('./output/data/proton_range.csv', index_col=None)
    # fit_poly(
    #     [
    #         proton_range_data['energy'].values,
    #         proton_range_data['range'].values
    #     ]
    # ) 
    plot.plot_range_en(proton_range_data, dens=True, fit=True)
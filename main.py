import os
from os import path
from modules.physics import *
from modules.plots import *
from modules.analyse import *
from modules.analyse import *
import pandas as pd

if __name__ == '__main__':
    # data = {'energy': [], 'range': []}
    # for en in range(1, 231):
    #     print(f'Starting energy: {en}')
    #     proton_range = get_proton_range(en)
    #     if proton_range != -1:
    #         data['energy'].append(en)
    #         data['range'].append(proton_range)
    #     print(f'Finished energy: {en}')
    # pd.DataFrame(data).to_csv('./output/data/proton_range.csv', index=None)
    # print(get_WEPL(80, 200, mat='dtc'))
    # proton_range_data =\
    #     pd.read_csv('./output/data/proton_range.csv', index_col=None)
    # fit_poly(
    #     [
    #         proton_range_data['energy'].values,
    #         proton_range_data['range'].values
    #     ]
    # ) 
from os import path
import matplotlib
matplotlib.rcParams['axes.unicode_minus'] = False
from matplotlib.colors import ListedColormap,LinearSegmentedColormap, Normalize
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Ellipse
from matplotlib.ticker import (MultipleLocator,
                               FormatStrFormatter,
                               AutoMinorLocator)
from matplotlib.lines import Line2D
from matplotlib import ticker
from scipy.optimize import curve_fit
from scipy import stats
import numpy.typing as npt
from typing import Any
import json

from modules import physics

OUTPUT_DIR = "./output/images"
FONT_SIZE = 28

plt.rcParams['font.family'] = "Times New Roman"
plt.rcParams['font.weight'] = 'bold'
plt.rcParams['font.size'] = FONT_SIZE

# Prevent math text from using a different font
plt.rcParams['mathtext.fontset'] = 'custom'
plt.rcParams['mathtext.rm'] = 'Times New Roman'  # Roman (serif) font
plt.rcParams['mathtext.it'] = 'Times New Roman:italic'  # Italic font
plt.rcParams['mathtext.bf'] = 'Times New Roman'  # Bold font
plt.rcParams['mathtext.sf'] = 'Times New Roman'  # Sans-serif font
plt.rcParams['mathtext.tt'] = 'Times New Roman'  # Monospace font

def plot_dtc_hits_2d(*args, **kwargs):
    if 'data' in kwargs.keys():
        data = kwargs['data']
    else:
        data = args[0]
    
    x_min = kwargs['x_min'] if 'x_min' in kwargs.keys() else int(min(data[:, 0]))
    x_max = kwargs['x_max'] if 'x_max' in kwargs.keys() else int(max(data[:, 0]))
    y_min = kwargs['y_min'] if 'y_min' in kwargs.keys() else int(min(data[:, 1]))
    y_max = kwargs['y_max'] if 'y_max' in kwargs.keys() else int(max(data[:, 1]))
    xbin = kwargs['xbin'] if 'xbin' in kwargs.keys() else 1
    ybin = kwargs['ybin'] if 'ybin' in kwargs.keys() else 1
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.hist2d(data[:, 0], data[:, 1], 
              bins=(range(x_min, x_max, xbin), range(y_min, y_max, ybin)))
    plt.savefig(f"""{OUTPUT_DIR}/{kwargs["name"] 
                if "name" in kwargs.keys() else "dtc_hits_2d.png"}""", dpi=300)
    # plt.show()

def plot_dtc_wepl_hist_1d(*args, **kwargs):
    if 'data' in kwargs.keys():
        data = kwargs['data']
    else:
        data = args[0]

    x_min = kwargs['x_min'] if 'x_min' in kwargs.keys() else int(min(data))
    x_max = kwargs['x_max'] if 'x_max' in kwargs.keys() else int(max(data))
    xbin = kwargs['xbin'] if 'xbin' in kwargs.keys() else 1
    fig, ax = plt.subplots(figsize=(12, 10))
    plt.hist(data, bins=range(x_min, x_max, xbin))
    plt.savefig(f"""{OUTPUT_DIR}/{kwargs["name"] if "name"
        in kwargs.keys() else "dtc_wepl_hits_1d.png"}""", dpi=300)

def plot_dtc_range(*args, **kwargs):
    if 'data' in kwargs.keys():
        data = kwargs['data']
    else:
        data = args[0]

    fig, ax = plt.subplots(figsize=(12, 10))
    ax.plot(data[0], data[1])
    ax.set_xlim([0, 1.1*max(data[0])])
    plt.savefig(f"""{OUTPUT_DIR}/{kwargs["name"] if "name"
        in kwargs.keys() else "dtc_range.png"}""", dpi=300)

def plot_entries_thickness_hist_1d(*args, **kwargs):
    if 'data' in kwargs.keys():
        data = kwargs['data']
    else:
        data = args[0]

    x_min = kwargs['x_min'] if 'x_min' in kwargs.keys() else int(min(data))
    x_max = kwargs['x_max'] if 'x_max' in kwargs.keys() else int(max(data))
    xbin = kwargs['xbin'] if 'xbin' in kwargs.keys() else 1
    fig, ax = plt.subplots(figsize=(12, 10))
    plt.hist(data, bins=range(x_min, x_max, xbin))
    plt.savefig(f"""{OUTPUT_DIR}/{kwargs["name"] if "name"
        in kwargs.keys() else "entries_thickness_hits_1d.png"}""", dpi=300)

def plot_range_en(*args, **kwargs):
    aluminium_dens = 2.7
    silicon_dens = 2.33
    air_dens = 0.0012
    avg_dens = (aluminium_dens*3.511 + silicon_dens*0.039 +
        air_dens*(25. - 3.511 - 0.039))/(25.)

    kwargs['dens'] = kwargs['dens'] if 'dens' in kwargs.keys() else False
    kwargs['fit'] = kwargs['fit'] if 'fit' in kwargs.keys() else False

    if 'data' in kwargs.keys():
        data = kwargs['data']
    else:
        data = args[0]
    
    thick_points = []
    if kwargs['fit']:
        thick_points = np.linspace(data['range'].min(), data['range'].max(), 100)
        kwargs['en-fit'] = np.array([physics.get_en_from_dtc(i) for i in thick_points])
        thick_points = thick_points*0.1

    data['range'] = data['range'].values*0.1

    if kwargs['dens']:
        data['range'] = data['range']*avg_dens
        thick_points = thick_points*avg_dens

        # kwargs['en-fit'] = physics.get_en_from_dtc(thick_points)\
        #     if not kwargs['dens'] else physics.get_en_from_dtc(thick_points)*avg_dens

    name = "proton_range_en" + ("_fit" if kwargs['fit'] else "")\
        + ("_dens" if kwargs['dens'] else "") + ".png"
     
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.scatter(data['energy'], data['range'], marker='o')
    if kwargs['fit']:
        ax.plot(kwargs['en-fit'], thick_points, c='r', linewidth=4, alpha=0.75)
    ax.set_title("Proton range", fontweight='bold')
    ax.set_xlabel("Energy ($MeV$)", fontweight='bold', loc='right')
    ax.set_ylabel("Range ($g/cm^2$)" if kwargs['dens'] else "Range ($cm$)",
                  fontweight='bold', loc='top')
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.tick_params(axis='both', which='major', 
                                            direction="in",
                                            width=2.5, length=14)
    ax.tick_params(axis='both', which='minor', 
                                            direction="in",
                                            width=1.5, length=6)
    plt.savefig(f"{OUTPUT_DIR}/{name}", dpi=300)
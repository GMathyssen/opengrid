# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 18:03:24 2014

@author: KDB
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.dates import DayLocator, AutoDateFormatter, date2num
from matplotlib.colors import LogNorm

def carpet(timeseries, vmax=None, vmin=None, zlabel=None, title=None):
    """
    Draw a carpet plot of a pandas timeseries.

    Parameters
    ----------
    timeseries : pandas.Series
    scale: sequence of numbers, e.g. np.linspace(0, 1000)
    """
    fig, ax = plt.subplots()
    ts = timeseries.resample('H', how='mean', label='left',closed='left')
    if vmin is None:
        vmin = ts.min()
    if vmax is None:
        vmax = ts.max()
    scale = np.linspace(vmin, vmax)

    ts.index = pd.MultiIndex.from_arrays([ts.index.hour, date2num(ts.index.date)])
    df = ts.unstack()
    mcolumns, mrows = np.meshgrid(df.columns, df.index)
    plt.contourf(mrows, mcolumns, df, scale, cmap=cm.coolwarm, norm=LogNorm())
    ax.yaxis_date()
    plt.xlabel('Hour of the day')
    plt.ylabel('Day of the year')

    ax.invert_yaxis()
    #ax.invert_yaxis() with a datetime axis obliterates the ticklocator and formatting settings
    #solution: see http://stackoverflow.com/questions/5804969/displaying-an-inverted-vertical-date-axis
    date_locator = DayLocator(interval=1)
    date_formatter = AutoDateFormatter(date_locator)
    ax.yaxis.set_major_locator(date_locator)
    ax.yaxis.set_major_formatter(date_formatter)

    ticks = np.linspace(scale[0], scale[-1], 11, endpoint=True)
    cb = plt.colorbar(format='%.2f',ticks=ticks)
    if zlabel is not None:
        cb.set_label(zlabel)
    elif timeseries.name:
        cb.set_label(timeseries.name)
    if title is not None:
        plt.title(title)
    elif timeseries.name:
        plt.title('carpet plot: ' + timeseries.name)

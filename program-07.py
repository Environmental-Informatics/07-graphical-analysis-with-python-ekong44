#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 22:51:33 2020
@author: kong44

Program Description: 
    This script accepts earthquake data in the form of a CSV file.
    The data is processed with the Panda and Matplotlib modules to generate plots. 
    
Reference Links: 
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.gaussian_kde.html#scipy.stats.gaussian_kde
    https://stackoverflow.com/questions/4150171/how-to-create-a-density-plot-in-matplotlib
    https://stackoverflow.com/questions/13865596/quantile-quantile-plot-using-scipy
"""

# importing modules
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np 
import scipy.stats as stats

# attempting genfromtxt 
#test_run = np.genfromtxt('all_month.csv', skip_header=1, delimiter=',')
print("\nGenfromtxt won't work since there are some rows that are missing data in columns.")

# reading in the data 
earth = pd.read_table('all_month.csv', header=0, sep=',')

# histogram of earthquake mag 
mag = earth['mag'].dropna() # ignoring the NAN's in the magnitude column
custom_bins = range(0,11,1)
plt.hist(mag, bins=custom_bins) 
plt.xlabel('Magnitude')
plt.ylabel('Frequency')
plt.title('Histogram of USGS Earthquake Data')
plt.savefig('hist.jpg')
plt.close() # so the plots don't overwrite each other on the same plot

# KDE of earthquake mag 
#kde = mag.plot.kde(ind=custom_bins, bw_method = 0.25)
kde = stats.gaussian_kde(mag)
spacing = np.linspace(0,10, num=500) #start,stop, and the number of points/samples between them
kde.covariance_factor = lambda : .25 # bandwidth adjustment
kde._compute_covariance()
plt.plot(spacing,kde(spacing))
plt.xlabel('Magnitude')
plt.ylabel('Frequency')
plt.title('KDE Plot of USGS Earthquake Data')
plt.savefig('kde.jpg')
plt.close()

# longitude vs latitude 
plt.scatter(earth['longitude'].dropna(),earth['latitude'].dropna(),s=5)
plt.xlabel('Longitude (decimal degrees)')
plt.ylabel('Latitude (decimal degrees)')
plt.title('Earthquakes on Planet Earth')
plt.savefig('earth.jpg')
plt.close()

# normalized cummulative distribution plot of earthquake depth 
sort_depth = np.sort(earth['depth'].dropna())
prob = np.linspace(0,1,len(sort_depth))
plt.plot(sort_depth, prob)
plt.xlabel('Depth (km)')
plt.ylabel('Probability')
plt.title('CDF of Earthquake Depth')
plt.savefig('cdf.jpg')
plt.close()

# Scatter plot of earthquake mag vs depth
plt.scatter(earth['mag'],earth['depth'],s=5)
plt.xlabel('Magnitude')
plt.ylabel('Depth (km)')
plt.title('Earthquake Magnitude vs. Depth')
plt.savefig('correlation.jpg')
plt.close()

# Quantile plot of earthquake mag 
stats.probplot(earth['mag'].dropna(), dist="norm", plot=plt)
plt.xlabel('Normal Quantiles')
plt.ylabel('Data Quantiles')
plt.title('Q-Q Plot of Earthquake Magnitudes')
plt.savefig('qq.jpg')
plt.close()
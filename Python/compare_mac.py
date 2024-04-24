#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 20:24:42 2022

@author: chethantulsidas
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import poisson,skellam

def poissongraph(df, league, season):
    print("\nPossion graph for {0} {1}/{2}".format(league,season,(season+1)%100))

    league = league.lower()
    df = df[(df["season"] == season) & (df["league"] == league)]
    #print(df.sample())

    # construct Poisson  for each mean goals value
    poisson_pred = np.column_stack([[poisson.pmf(i, df.mean()[j]) for i in range(8)] for j in range(2)])

    # plot histogram of actual goals
    plt.hist(df[['homeScore', 'awayScore']].values, range(9), alpha=0.7, label=['Home', 'Away'], color=["#9067A7", "#84BA5B"], density=True)

    # add lines for the Poisson distributions
    pois1, = plt.plot([i-0.5 for i in range(1,9)], poisson_pred[:,0], linestyle='-', marker='o',label="Home", color = '#6B4C9A')
    pois2, = plt.plot([i-0.5 for i in range(1,9)], poisson_pred[:,1], linestyle='-', marker='o',label="Away", color = '#3E9651')

    leg=plt.legend(loc='upper right', fontsize=13, ncol=2)
    leg.set_title("Poisson           Actual        ", prop = {'size':'14', 'weight':'bold'})

    plt.xticks([i-0.5 for i in range(1,9)],[i for i in range(9)])
    plt.xlabel("Goals per Match",size=13)
    plt.ylabel("Proportion of Matches",size=13)
    #plt.title("Number of Goals per Match\n{0} {1}/{2} Season".format(league,season,(season+1)%100),size=14,fontweight='bold')
    plt.ylim([-0.004, 0.4])
    plt.tight_layout()
    plt.show()

def skellamgraph(df, league, season):
    print("Skellam grpah for {0} {1}/{2} Season".format(league,season,(season+1)%100))
    df = df.loc[df["season"] == season]
    skellam_pred = [skellam.pmf(i,  df.mean()[0],  df.mean()[1]) for i in range(-6,8)]
    plt.hist(df[['homeScore']].values - df[['awayScore']].values, range(-6,8), alpha=0.7, label='Actual',normed=True, color = '#D35E60')
    plt.plot([i+0.5 for i in range(-6,8)], skellam_pred, linestyle='-', marker='o',label="Skellam", color = '#396AB1')
    plt.legend(loc='upper right', fontsize=13)
    plt.xticks([i+0.5 for i in range(-6,8)],[i for i in range(-6,8)])
    plt.xlabel("Home Goals - Away Goals",size=13)
    plt.ylabel("Proportion of Matches",size=13)
    plt.title("Difference in Goals Scored (Home Team vs Away Team)\n{0} {1}/{2} Season".format(league,season,(season+1)%100),size=14,fontweight='bold')
    plt.ylim([-0.004, 0.30])
    plt.tight_layout()
    plt.show()
    

#filename = "data/spain.csv"
#data = pd.read_csv(filename)
#poissongraph(data, "LaLiga", 2019)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 17:06:14 2022

@author: chethantulsidas
"""


import scrape_mac
import compare_mac
import stats_mac
import predict_mac
import datetime
from IPython import get_ipython




countries = {1: "England", 2: "Spain", 3: "Germany", 4: "Italy", 5: "France"}

leagues = {1: {1: "Premier League", 2: "Championship", 3: "League One", 4: "League Two"}, 
           2: {1: "LaLiga", 2: "LaLiga2"}, 
           3: {1: "Bundesliga", 2: "2. Bundesliga", 3: "3. Liga"}, 
           4: {1: "Serie A", 2: "Serie B"}, 
           5: {1: "Ligue 1", 2: "Ligue 2", 3: "National"}}

repeat = 'y'

current_season = datetime.date.today().year



while(repeat == 'y' or repeat == 'Y'):
    
    try:
        get_ipython().magic('clear')
        get_ipython().magic('reset -f')
    except:
        pass

    print("\n\nWelcome to Assist\n")
    
    #data = pd.DataFrame()
    

    print("\nPick a country : ")
    for i, country_name in countries.items():
        print("{0}. {1}".format(i, country_name))
    
    country_choice = int(input("Enter your choice : "))
    

    #print("\nPick a league : ")
    #print("")
    #for i, league_name in leagues[country_choice].items():
        #print("{0}. {1}".format(i, league_name))
        
    #league_choice = int(input("Enter your choice : "))
    
    country = countries[country_choice]
    #league = leagues[country_choice][league_choice]
    
    
    #print("\nCountry : {0}\nLeague : {1}".format(country, league))
        
    #for i, league in leagues[country_choice].items():
       #print(league)

    flag, filename = scrape_mac.checkdata(country)
    print("")
    #print(flag, filename)
 
    #print(flag)
    
    if (flag == -1):
        print(country + " league data unavailable")
        data = scrape_mac.get_data(country_choice, filename)

    else:
        print(country + " league data available from the {0}/{1} season".format(flag, (flag + 1)%100))
        update_choice = input("Update league data? (y/n) : ")
        #print()
        if (update_choice == "y" or update_choice == "Y"):
            data = scrape_mac.get_data(country_choice, filename)
            #print("Update Competition Data")
        else:
            data = scrape_mac.get_data(country_choice, filename, flag)
            #data = scrape.getcompetitiondata(country, league)
            #print("Get Competition Data")
            
    print("\n\n-----------------------------------------------------------")

    print("\n\nPick a league : ")
    for i, league_name in leagues[country_choice].items():
        print("{0}. {1}".format(i, league_name))    
    league_choice = int(input("Enter your choice : "))
    
    league = leagues[country_choice][league_choice]
    

    season = int(input("Enter test season (yyyy) : "))
    print("\nYou have chosen {0} {1}/{2}".format(league, season, (season + 1) % 100))


    func_choice = -1
    while (func_choice != 0):
        input()
        
        try:
            get_ipython().magic('clear')
            get_ipython().magic('reset -f')
        except:
            pass
        
        print("\n\n")
        print(country, league, season)
        #print("\n---------------------------------------\n\n")
        print("\n\nPick a function : ")
        print("1.Compare predicted and historical data")
        print("2.Explore league statistics")
        print("3.Explore team statistics")
        print("4.Predict match")
        print("0.Exit\n")
        func_choice = int(input("Enter your choice : "))
        
        try:
            get_ipython().magic('clear')
            get_ipython().magic('reset -f')
        except:
            pass
        
        if func_choice == 0:
            break
        elif func_choice == 1:
            compare_mac.poissongraph(data, league, season)
            #compare_mac.skellamgraph(data, league, season)
        elif func_choice == 2:
            stats_mac.leaguestats(data, league, season)
        elif func_choice == 3:
            stats_mac.teamstats(data, league, season)
        elif func_choice == 4:
            homeTeam, awayTeam = predict_mac.teamnames(data, league, season)
            predict_mac.predict(data, league, season, homeTeam, awayTeam)
        else:
            break
            


    repeat = (input("Pick another country? (y/n) : "))
    print("\n---------------------------------------")
    

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 20:25:00 2022

@author: chethantulsidas
"""

import numpy as np
import pandas as pd
import datetime
import statistics as st
import math
import random


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def teamnames(data, league, season):
    
    try:
        get_ipython().magic('clear')
        get_ipython().magic('reset -f')
    except:
        pass
    
    print("\n\n")
    
    print("{0} {1}/{2}".format(league, season, (season+1)%100))
    
    print("\n\n")
    
    league = league.lower()
    teams = data[(data["league"] == league) & (data["season"] == season)]
    teams = list(teams["homeTeam"].unique())
    #print(type(teams))
    teams.sort()
    i = 0
    for team in teams:
        #print("{0}.{1}".format(i, team))
        i = i + 1
        print("{:<25}".format(str(i) + "." + team), end="")
        if (((i) % 4) == 0):
            print("\n")    
            
    print("")
    home_choice = int(input("Pick Home team : "))
    away_choice = int(input("Pick Away team : "))
    
    homeTeam = teams[home_choice-1]
    awayTeam = teams[away_choice-1]
    
    return homeTeam, awayTeam
    


def predict(data, league, season, homeTeam, awayTeam, league_history=380, team_history=19, display=0):
    
    simulatedgames = 10000
    
    
    league = league.lower()
    
    
    game = data[(data["homeTeam"] == homeTeam) & (data["awayTeam"] == awayTeam) & (data["season"] == season)]
    homeReal = game["homeScore"].values[0]
    awayReal = game["awayScore"].values[0]
    matchdate = game["date"].values[0]


    
    
    
    league_data = data[(data["date"] < matchdate) & (data["league"] == league)]
    #home_data = data[(data["date"] < matchdate) & (data["homeTeam"] == homeTeam) & (data["league"] == league) & (data["season"] >= season-1)]
    #away_data = data[(data["date"] < matchdate) & (data["awayTeam"] == awayTeam) & (data["league"] == league) & (data["season"] >= season-1)]
    
    home_data = data[(data["date"] < matchdate) & (data["homeTeam"] == homeTeam)]
    away_data = data[(data["date"] < matchdate) & (data["awayTeam"] == awayTeam)]
    
    league_data = league_data.head(league_history)
    home_data = home_data.head(team_history)
    away_data = away_data.head(team_history)
    
    #print(league_data.shape)
    #print(home_data.shape)
    #print(away_data.shape)
    
    #print(league_data.head(3))
    #print(home_data.head(3))
    #print(away_data.head(3))
    
    
    homeZero = round((league_data[league_data["homeScore"] == 0].shape[0] / league_history) * 100, 2)
    awayZero = round((league_data[league_data["awayScore"] == 0].shape[0] / league_history) * 100, 2)
    
    #homeZero = round((home_data[home_data["homeScore"] == 0].shape[0] / team_history) * 100, 2)
    #awayZero = round((away_data[away_data["awayScore"] == 0].shape[0] / team_history) * 100, 2)
    
    
    
    homeAvg = round(league_data["homeScore"].mean(), 2)
    awayAvg = round(league_data["awayScore"].mean(), 2)
    

    
    homeTeamAvgFor = round(home_data["homeScore"].mean(), 2)
    homeTeamAvgAgainst = round(home_data["awayScore"].mean(), 2)
    homeTeamAttackStrength = round(homeTeamAvgFor / homeAvg, 2)
    homeTeamDefenseStrength = round(homeTeamAvgAgainst / awayAvg, 2)
    
    
    
    
    awayTeamAvgFor = round(away_data["awayScore"].mean(), 2)
    awayTeamAvgAgainst = round(away_data["homeScore"].mean(), 2)
    awayTeamAttackStrength = round(awayTeamAvgFor / awayAvg, 2)
    awayTeamDefenseStrength = round(awayTeamAvgAgainst / homeAvg, 2)
    
    
    if math.isnan(homeTeamAvgFor):
        #print("Home :", homeTeam)
        #print("Away :", awayTeam)
        homeTeamAvgFor = 0
        homeTeamAvgAgainst = 0
        homeTeamAttackStrength = 1
        homeTeamDefenseStrength = 1
        
    if math.isnan(awayTeamAvgFor):
        #print("Away :",awayTeam)
        #print("Home :", homeTeam)
        awayTeamAvgFor = 0
        awayTeamAvgAgainst = 0
        awayTeamAttackStrength = 1
        awayTeamDefenseStrength = 1
        
    if homeTeamAvgFor == 0:
        homeTeamAttackStrength = 1
        
    if awayTeamAvgFor == 0:
        awayTeamAttackStrength = 1
        
        
    if homeTeamAvgAgainst == 0:
        homeTeamDefenseStrength = 1
    
    if awayTeamAvgAgainst == 0:
        awayTeamDefenseStrength = 1
    
    
    
    
    
    homeTeamExpectedGoals = round(homeTeamAttackStrength * awayTeamDefenseStrength * homeAvg, 2)
    awayTeamExpectedGoals = round(awayTeamAttackStrength * homeTeamDefenseStrength * awayAvg, 2)
    
    
    
    
    
    homeTeamPoisson = np.random.poisson(homeTeamExpectedGoals, simulatedgames)
    awayTeamPoisson = np.random.poisson(awayTeamExpectedGoals, simulatedgames)
    
    unique_home, count_home = np.unique(homeTeamPoisson, return_counts=True)
    unique_away, count_away = np.unique(awayTeamPoisson, return_counts=True)

    
    
    homeMode = st.mode(homeTeamPoisson)
    awayMode = st.mode(awayTeamPoisson)
    
    homeMean = np.sum(homeTeamPoisson)/simulatedgames
    awayMean = np.sum(awayTeamPoisson)/simulatedgames
    
    
    
    
    #homeRandom = np.random.choice(homeTeamPoisson)
    #awayRandom = np.random.choice(awayTeamPoisson)
    
    #homeRandom = np.sum(homeRandom)/100
    #awayRandom = np.sum(awayRandom)/100
    
    rand_home = random.randint(0, simulatedgames-1)
    rand_away = random.randint(0, simulatedgames-1)
    
    homeRandom = homeTeamPoisson[rand_home]
    awayRandom = awayTeamPoisson[rand_away]
    
    homeZIP = homeMean
    awayZIP = awayMean
    
    if rand_home < homeZero*100:
        homeZIP = 0
    if rand_away < awayZero*100:
        awayZIP = 0
    
    
    
    
    homeTeamWins = round(np.sum(homeTeamPoisson > awayTeamPoisson) / simulatedgames * 100, 2)
    draw = round(np.sum(homeTeamPoisson == awayTeamPoisson) / simulatedgames * 100, 2)
    awayTeamWins = round(np.sum(homeTeamPoisson < awayTeamPoisson) / simulatedgames * 100, 2)
    over = round(np.sum((homeTeamPoisson + awayTeamPoisson) >= 2.5) / simulatedgames * 100, 2)
    bothTeamsScore = round(np.sum((homeTeamPoisson > 0) & (awayTeamPoisson > 0)) / simulatedgames * 100, 2)
    
    
    
    
    
    
    rand_game = random.randint(0, simulatedgames-1)
    
    if rand_game < homeTeamWins*100:
        result = "Home"
    elif (rand_game >= homeTeamWins*100) & (rand_game < ((homeTeamWins + draw)*100)):
        result = "Draw"
    else:
        result = "Away"
    
    
    
    homeTeamOdds = round(100 / homeTeamWins, 2)
    drawOdds = round(100 / draw, 2)
    awayTeamOdds = round(100 / awayTeamWins, 2)
    overOdds = round(100 / over, 2)
    bothTeamsScoreOdds = round(100 / bothTeamsScore, 2)
    
    
    #if homeMode > awayMode:
        #result = homeTeam + " wins"
    #elif homeMode == awayMode:
        #result = "Draw"
    #elif homeMode < awayMode:
        #result = awayTeam + " wins"
               
    
    if display == 1:
    
        try:
            get_ipython().magic('clear')
            get_ipython().magic('reset -f')
        except:
                pass    
    
        print("\n\n" + homeTeam + " vs. " + awayTeam)
    
        #print(game.info())
        print("Scoreline :", homeReal, "-", awayReal)
        print("Date :", matchdate)
        print("\n")
        #print(game)
        
        print("League average goals")
        print("Home team :", homeAvg)
        print("Away team :", awayAvg)
        
        #print("\nZero goals")
        #print("Home team : {0}%".format(homeZero))
        #print("Away team : {0}%".format(awayZero))
        
        print("\n\nHome team")
        print("Average goals scored :", homeTeamAvgFor)
        print("Average goals conceded :", homeTeamAvgAgainst)
        print("Attack strength :", homeTeamAttackStrength)
        print("Defense strength :", homeTeamDefenseStrength)
        
        print("\n\nAway team")
        print("Average goals scored :", awayTeamAvgFor)
        print("Average goals conceded :", awayTeamAvgAgainst)
        print("Attack strength :", awayTeamAttackStrength)
        print("Defense strength :", awayTeamDefenseStrength)
    
    
        print("\n\nExpected goals")
        print("Home team :", homeTeamExpectedGoals)
        print("Away team :", awayTeamExpectedGoals)
        #print(round(homeTeamExpectedGoals))
        #print(round(awayTeamExpectedGoals))
        
        print("\n\nHome team poisson")
        print(np.asarray((unique_home, count_home)))
        print("\n\nAway team poisson")
        print(np.asarray((unique_away, count_away)))
        
        #print(homeTeamPoisson)
        #print(awayTeamPoisson)
            

        print("\n\nPredictions")
        #print("Home team :", homeTeamWins)
        #print("Draw :", draw)
        #print("Away team :", awayTeamWins)
        #print("Over 2.5 :", over)
        #print("Both teams score :", bothTeamsScore)
    
    
        print(f"{'Home team :':<20}{homeTeamWins:>5}{'%'}{'|':^9}{homeTeamOdds:>5}")
        print(f"{'Draw :':<20}{draw:>5}{'%'}{'|':^9}{drawOdds:>5}")
        print(f"{'Away team :':<20}{awayTeamWins:>5}{'%'}{'|':^9}{awayTeamOdds:>5}")
        print(f"{'Over 2.5 :':<20}{over:>5}{'%'}{'|':^9}{overOdds:>5}")
        print(f"{'Both teams score :':<20}{bothTeamsScore:>5}{'%'}{'|':^9}{bothTeamsScoreOdds:>5}")
        
        #print("\n\nRand :", rand_game)
        #print("Rand result :", result)
        
        
        #print("\n\nMode result : {0}-{1}".format(homeMode, awayMode))
        
        #print("\n\nRandom result : {0}-{1}".format(homeRandom, awayRandom))
        
        #print("\n\nMean result : {0}-{1}".format(homeMean, awayMean))
        
        #print("\n\nZIP result : {0} - {1}".format(homeZIP, awayZIP))
        
        #print(result)
            
    #return homeMode, awayMode

    #return homeRandom, awayRandom

    return homeMean, awayMean

    #return homeZIP, awayZIP
    
    #return result
    

def leaguepredict(data, league, season):
    
    try:
        get_ipython().magic('clear')
        get_ipython().magic('reset -f')
    except:
        pass
    
    
    print("\n\n{0} {1}/{2} Predictions\n".format(league, season, (season+1)%100))
    
    league = league.lower()
    teams = data[(data["league"] == league) & (data["season"] == season)]
    teams = list(teams["homeTeam"].unique())
    #print(type(teams))
    teams.sort()
    
    col = ["Team", "W", "D", "L", "Points"]
    df = pd.DataFrame(columns = col)
    
    
    i = 0
    for team in teams:
        dict = {"Team" : team, "W" : 0, "D" : 0, "L" : 0, "Points" : 0}
        df = df.append(dict, ignore_index=True)
        #teamdata = pd.DataFrame([team, 0,0,0])
        #df = df.append(teamdata, ignore_index=True)
        
    #print(df)
    
    #print("\n")
    
    league_data = data[(data["league"] == league) & (data["season"] <= season)]
    #league_data = league_data.sort_values("date")
    #print(league_data.head(5))
    #print("\n")
    #print(league_data.tail(5))
    
    #print("\n")
    
    match_data = data[(data["league"] == league) & (data["season"] == season)]
    match_data = match_data.sort_values("date")
    #print(match_data.head(5))
    #print("\n")
    #print(match_data.tail(5))
    
    matches = match_data.shape[0]
    #print("matches :", matches)
    
    for index, match in match_data.iterrows():
        
        #print(match)
        homeTeam = match["homeTeam"]
        awayTeam = match["awayTeam"]
        
        #print(homeTeam, awayTeam)
        
        homeScore, awayScore = predict(league_data, league, season, homeTeam, awayTeam, league_history=matches)
            
        if homeScore > awayScore:
            df.loc[df["Team"] == homeTeam, "W"] = df.loc[df["Team"] == homeTeam, "W"] + 1
            df.loc[df["Team"] == awayTeam, "L"] = df.loc[df["Team"] == awayTeam, "L"] + 1
            df.loc[df["Team"] == homeTeam, "Points"] = df.loc[df["Team"] == homeTeam, "Points"] + 3
            
        elif homeScore == awayScore:
            df.loc[df["Team"] == homeTeam, "D"] = df.loc[df["Team"] == homeTeam, "D"] + 1
            df.loc[df["Team"] == awayTeam, "D"] = df.loc[df["Team"] == awayTeam, "D"] + 1
            df.loc[df["Team"] == homeTeam, "Points"] = df.loc[df["Team"] == homeTeam, "Points"] + 1
            df.loc[df["Team"] == awayTeam, "Points"] = df.loc[df["Team"] == awayTeam, "Points"] + 1
            
        elif homeScore < awayScore : 
            df.loc[df["Team"] == awayTeam, "W"] = df.loc[df["Team"] == awayTeam, "W"] + 1
            df.loc[df["Team"] == homeTeam, "L"] = df.loc[df["Team"] == homeTeam, "L"] + 1
            df.loc[df["Team"] == awayTeam, "Points"] = df.loc[df["Team"] == awayTeam, "Points"] + 3
            
        
        league_data.loc[(league_data["homeTeam"] == homeTeam) & (league_data["awayTeam"] == awayTeam) & (league_data["season"] == season), "homeScore"] == homeScore
        league_data.loc[(league_data["homeTeam"] == homeTeam) & (league_data["awayTeam"] == awayTeam) & (league_data["season"] == season), "awayScore"] == awayScore
    
    
    df = df.sort_values(by="Points", ascending=False, ignore_index=True)
    
    df.index = df.index+1
    
    print(df)
    
    #print(df.to_string(index = False))
    
        
    """
    
    for homeTeam in teams:
        for awayTeam in teams:
            
            if homeTeam == awayTeam:
                continue
            
            homeScore, awayScore = predict(data, league, season, homeTeam, awayTeam)
            
            if homeScore > awayScore:
                df.loc[df["Team"] == homeTeam, "W"] = df.loc[df["Team"] == homeTeam, "W"] + 1
                df.loc[df["Team"] == awayTeam, "L"] = df.loc[df["Team"] == awayTeam, "L"] + 1
                df.loc[df["Team"] == homeTeam, "Points"] = df.loc[df["Team"] == homeTeam, "Points"] + 3
                
            elif homeScore == awayScore:
                df.loc[df["Team"] == homeTeam, "D"] = df.loc[df["Team"] == homeTeam, "D"] + 1
                df.loc[df["Team"] == awayTeam, "D"] = df.loc[df["Team"] == awayTeam, "D"] + 1
                df.loc[df["Team"] == homeTeam, "Points"] = df.loc[df["Team"] == homeTeam, "Points"] + 1
                df.loc[df["Team"] == awayTeam, "Points"] = df.loc[df["Team"] == awayTeam, "Points"] + 3
                
            elif homeScore < awayScore : 
                df.loc[df["Team"] == awayTeam, "W"] = df.loc[df["Team"] == awayTeam, "W"] + 1
                df.loc[df["Team"] == homeTeam, "L"] = df.loc[df["Team"] == homeTeam, "L"] + 1
                df.loc[df["Team"] == awayTeam, "Points"] = df.loc[df["Team"] == awayTeam, "Points"] + 3
        
    df = df.sort_values(by="Points", ascending=False, ignore_index=True)
    
    print(df)
    
    
    """
        
            
        
        
    


def leaguestrength(data, league, season):
    
    try:
        get_ipython().magic('clear')
        get_ipython().magic('reset -f')
    except:
        pass
    
    
    print("\n\n{0} {1}/{2} Strength\n".format(league, season, (season+1)%100))

    
    league = league.lower()
    teams = data[(data["league"] == league) & (data["season"] == season)]
    teams = list(teams["homeTeam"].unique())
    #print(type(teams))
    teams.sort()
    
    league_data = data[(data["league"] == league) & (data["season"] == season)]
    
    
    #print(league_data["homeScore"].sum())
    #print(league_data["awayScore"].sum())
    
    homeAvg = round(league_data["homeScore"].mean(), 2)
    awayAvg = round(league_data["awayScore"].mean(), 2)
    
    print("League Home Avg. :", homeAvg)
    print("League Away Avg :", awayAvg)
    
    
    
    
    print(f"\n\n{'Team':<15}{'HomeAttk':>9}{'HomeDfns':>9}{'':^5}{'AwayAttk':>9}{'AwayDfns':>9}")
    
    for team in teams:
         
        home_data = league_data[league_data["homeTeam"] == team]
        away_data = league_data[league_data["awayTeam"] == team]
         #print("League average goals")
         #print("Home team :", homeAvg)
         #print("Away team :", awayAvg)
    
        homeTeamAvgFor = round(home_data["homeScore"].mean(), 2)
        homeTeamAvgAgainst = round(home_data["awayScore"].mean(), 2)
        homeTeamAttackStrength = round(homeTeamAvgFor / homeAvg, 2)
        homeTeamDefenseStrength = round(homeTeamAvgAgainst / awayAvg, 2)
    
    
    
        awayTeamAvgFor = round(away_data["awayScore"].mean(), 2)
        awayTeamAvgAgainst = round(away_data["homeScore"].mean(), 2)
        awayTeamAttackStrength = round(awayTeamAvgFor / awayAvg, 2)
        awayTeamDefenseStrength = round(awayTeamAvgAgainst / homeAvg, 2)
        
        #print(awayTeamAvgFor, away_data["awayScore"].sum())
    
        #print(team, homeTeamAttackStrength, homeTeamDefenseStrength, awayTeamAttackStrength, awayTeamDefenseStrength)
        

        print(f"{team:<15}{homeTeamAttackStrength:>9}{homeTeamDefenseStrength:>9}{'':^5}{awayTeamAttackStrength:>9}{awayTeamDefenseStrength:>9}")
        
        
    

def result(x, y):
    if x > y:
        return("Home")
    elif x < y:
        return("Away")
    elif x == y:
        return("Draw")



def accuracy(data, league, season, display=0):

    try:
        get_ipython().magic('clear')
        get_ipython().magic('reset -f')
    except:
        pass
    
    
    print("\n\n{0} {1}/{2} Accuracy\n".format(league, season, (season+1)%100))

    
    league = league.lower()
    teams = data[(data["league"] == league) & (data["season"] == season)]
    teams = list(teams["homeTeam"].unique())
    #print(type(teams))
    teams.sort()    
    
    
    league_data = data[(data["league"] == league) & (data["season"] == season)]
    
    matches = league_data.shape[0]
    #print("matches :", matches)
    
    #print(league_data.shape, "\n")
    
    
    count = pred_win_count = real_win_count = pred_home = pred_draw = pred_away = real_home = real_draw = real_away = 0
    
    for homeTeam in teams:
        for awayTeam in teams:
            
            if homeTeam == awayTeam:
                continue
            #print("\n")
            #print(homeTeam, "vs.", awayTeam)
            
            homeScore, awayScore = predict(data, league, season, homeTeam, awayTeam, league_history=matches)

            
            if (homeScore > awayScore) | (awayScore > homeScore):
                pred_win_count = pred_win_count + 1
            
            pred_result = result(homeScore, awayScore)
            
            
            homeReal = int(league_data.loc[((league_data["homeTeam"] == homeTeam) & (league_data["awayTeam"] == awayTeam)), "homeScore"])
            awayReal = int(league_data.loc[((league_data["homeTeam"] == homeTeam) & (league_data["awayTeam"] == awayTeam)), "awayScore"])
            
            
            if (homeReal > awayReal) | (awayReal > homeReal):
                real_win_count = real_win_count + 1
            
            
            real_result = result(homeReal, awayReal)
            
            if pred_result == real_result:
                count = count+1
                #print("\n")
                #print(homeTeam, "vs.", awayTeam)
                #print("Predicted : {0} - {1}".format(homeScore, awayScore))
                #print("Real result : {0} - {1}".format(homeReal, awayReal))
                

                
    acc = round((count/matches)*100, 2)         
                
    if display == 1:
            
        #print(league_data.sample(5))
        #print(i)  
        #print("\n")
        print("No. of matches :", matches)
        print("Predicted win count :", pred_win_count)
        print("Real win count :", real_win_count)
        print("Correct count :", count)
        print("Accuracy :", acc)
    
    return acc

"""            
            pred_result = predict(data, league, season, homeTeam, awayTeam, league_history=matches)
            
            homeReal = int(league_data.loc[((league_data["homeTeam"] == homeTeam) & (league_data["awayTeam"] == awayTeam)), "homeScore"])
            awayReal = int(league_data.loc[((league_data["homeTeam"] == homeTeam) & (league_data["awayTeam"] == awayTeam)), "awayScore"])
            
            real_result = result(homeReal, awayReal)
            
            if pred_result == "Home":
                pred_home = pred_home + 1
            elif pred_result == "Draw":
                pred_draw = pred_draw + 1
            elif pred_result == "Away":
                pred_away = pred_away + 1
                
            if real_result == "Home":
                real_home = real_home + 1
            elif real_result == "Draw":
                real_draw = real_draw + 1
            elif real_result == "Away":
                real_away = real_away + 1
                
                
            if pred_result == real_result:
                count = count + 1
                #print(homeTeam, "vs.", awayTeam)
                
        
    acc = round((count/matches)*100, 2)
        
    print("\nNo. of matches :", matches)    
        
        
    print("\nPredicted results")
    print("Home wins :", pred_home)
    print("Draws :", pred_draw)
    print("Away wins :", pred_away)
    
    print("\n\nActual results")
    print("Home wins :", real_home)
    print("Draws :", real_draw)
    print("Away wins :", real_away)
    
    print("Correct predictions :", count)
    print("Accuracy : ", acc)
            
            
            
"""


    

    
    
filename = "data/england.csv"
league = "Premier League"
season = 2021
data = pd.read_csv(filename)


homeTeam, awayTeam = teamnames(data, league, season)
predict(data, league, season, homeTeam, awayTeam, display=1)

#leaguestrength(data, league, season)

#leaguepredict(data, league, season) 

#accuracy(data, league, season, display=1)














  
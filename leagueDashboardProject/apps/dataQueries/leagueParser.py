import re
import mwclient
import pandas as pd 
import numpy as np
import datetime as dt
from datetime import date, timedelta, datetime
from leagueDashboardProject import tidydata as td
import sys

date = datetime.date(datetime.now())
site  = mwclient.Site('lol.gamepedia.com', path = '/')
    
def searches():
    response = site.api('cargoquery',
                        limit = 'max',
                        tables = 'Tournaments = TN',
                        fields = "TN.Name, TN.Region, TN.Year, TN.IsOfficial, TN.IsQualifier, TN.IsPlayoffs, TN.Split, TN.SplitNumber, TN.DateStart",
                        where = 'TN.Year = "2020" AND TN.IsOfficial = 1 AND TN.DateStart <= "{} 00:00:00"'.format(str(date)),
                        order_by = 'TN.DateStart DESC')

    search_dictionary = {'Regions':{}, 'Qualifiers':[],'PlayOffs':[]}

    for dictionary in response['cargoquery']:
        if dictionary['title']['Region'] in search_dictionary['Regions']:
            pass
        else:
            search_dictionary['Regions'][dictionary['title']['Region']] = [] 
        
        if dictionary['title']['Region'] in list(search_dictionary['Regions'].keys()):
            search_dictionary['Regions'][dictionary['title']['Region']].append(dictionary['title']['Name'])
        if dictionary['title']['IsQualifier'] == "1":
                search_dictionary['Qualifiers'].append(dictionary['title']['Name'])
        
        if dictionary['title']['IsPlayoffs'] == "1":
                search_dictionary['PlayOffs'].append(dictionary['title']['Name'])
    return search_dictionary 

def defaultStandings(tournament = None):
    try: 
        defaultStanding = site.api('cargoquery',
                                        limit = 'max',
                                        tables = 'TournamentResults = TNR',
                                        fields = "TNR.Event,TNR.Place_Number,TNR.Team,TNR.UniqueLine",
                                        where = 'TNR.Event="{}"'.format(tournament)

                                    )
        standings = {}
        teams = 0 
        headers_standings = ['Event', 'Team', 'Place','UniqueLine']
        for team in defaultStanding['cargoquery']:
            standings[teams] = []
            standings[teams].append(team['title']['Event'])
            standings[teams].append(team['title']['Team'])
            standings[teams].append(team['title']['Place Number'])
            standings[teams].append(team['title']['UniqueLine'])
            teams += 1
        standings_df = pd.DataFrame.from_dict(standings, orient = 'index', columns = headers_standings)
        return standings_df
    except TypeError:
        print('Please Select the Tournament Standing you Would like to View')
        pass
    
def defaultHistoricalStanding(tournament = None):
    """
        Makes Historical Standing of regions
        Try the table ScoreboardGame
    """
    try:            
        defaultHistoricalStanding = site.api('cargoquery',
                                                limit = 'max',
                                                tables = 'ScoreboardGames = SG',
                                                fields = 'SG.Tournament, SG.Team1, SG.Team2, SG.WinTeam, SG.LossTeam,SG.Team1Score, SG.Team2Score, SG.Winner,SG.UniqueGame, SG.ScoreboardID_Wiki, SG.Gamename, SG.DateTime_UTC, SG.Team1Gold, SG.Team2Gold, SG.Team1Kills, SG.Team2Kills, SG.Team1RiftHeralds, SG.Team2RiftHeralds, SG.Team1Dragons, SG.Team2Dragons, SG.Team1Barons, SG.Team2Barons, SG.Team1Towers, SG.Team2Towers, SG.Team1Inhibitors, SG.Team2Inhibitors, SG.Gamelength',
                                                where = 'SG.Tournament="{}"'.format(tournament)
                                                )        
    except TypeError:
        print >> sys.stderr, 'Tournament Could not be found'
        print >> sys.stderr, 'Please Pick another Tournament'
        sys.exit(1)
    games = []
    for order_dic in defaultHistoricalStanding['cargoquery']:
        row_dict = {}
        for keys in order_dic['title'].keys():
            row_dict.update({keys : order_dic['title'][keys]})
        games.append(row_dict)
    games_df = pd.DataFrame(games)
    games_df = pd.melt(games_df, id_vars = games_df.columns.difference(['Team1','Team2']),
                 value_vars=['Team1','Team2'], var_name = 'Side', value_name = "Team")
    id_vars = list(games_df.columns.values) 
    games_df = td.superMelt(games_df,id_vars, [['Team1Barons','Team2Barons'],['Team1Dragons','Team2Dragons'],['Team1Gold','Team2Gold'],
                                        ['Team1Inhibitors','Team2Inhibitors'],['Team1Kills','Team2Kills'],['Team1RiftHeralds','Team2RiftHeralds'],
                                        ['Team1Score','Team2Score'],['Team1Towers','Team2Towers']],
                                        ['SideBarons','SideDragons','SideGold','SideInhibitors','SideKills','SideRiftHeralds','SideScore','SideTowers'],
                                       ['Barons','Dragons','Gold','Inhibitors','Kills','RiftHeralds','Score','Towers'])
    games_df['Side'] = games_df['Side'].map({'Team1':'Blue', 'Team2':'Red'})
    games_df['Winner'] = np.where(games_df['Winner']=='1', 'Blue', 'Red')
    games_df['Won'] = np.where(games_df['Side']==games_df['Winner'], '1', '0')
    games_df['TeamAgaints'] = np.where(games_df['WinTeam']==games_df['Team'], games_df['LossTeam'], games_df['WinTeam'])
    del games_df['WinTeam']
    del games_df['UniqueGame']
    del games_df['LossTeam']
    del games_df['DateTime UTC__precision']
    games_df = games_df.sort_values(by=['DateTime UTC'])
    games_df = games_df.reset_index()
    del games_df['index']
    for convert_columns in list(games_df.columns):
        if convert_columns in ['Barons','Dragons','Gold','RiftHeralds','Kills']:
            games_df[convert_columns] = pd.to_numeric(games_df[convert_columns])    
    return games_df

def statsDataFrames(tournament = None): 
    try:
        statsQuery = site.api('cargoquery',
                                limit = 'max',
                                tables = 'PicksAndBansS7, MatchScheduleGame, ScoreboardGames',
                                fields = 'PicksAndBansS7.Team1Role1, PicksAndBansS7.Team1Role2, PicksAndBansS7.Team1Role3, PicksAndBansS7.Team1Role4, PicksAndBansS7.Team1Role5, PicksAndBansS7.Team2Role1, PicksAndBansS7.Team2Role2, PicksAndBansS7.Team2Role3, PicksAndBansS7.Team2Role4, PicksAndBansS7.Team2Role5, PicksAndBansS7.Team1Ban1, PicksAndBansS7.Team1Ban2, PicksAndBansS7.Team1Ban3, PicksAndBansS7.Team1Ban4, PicksAndBansS7.Team1Ban5, PicksAndBansS7.Team1Pick1, PicksAndBansS7.Team1Pick2, PicksAndBansS7.Team1Pick3, PicksAndBansS7.Team1Pick4, PicksAndBansS7.Team1Pick5, PicksAndBansS7.Team2Ban1, PicksAndBansS7.Team2Ban2, PicksAndBansS7.Team2Ban3, PicksAndBansS7.Team2Ban4, PicksAndBansS7.Team2Ban5, PicksAndBansS7.Team2Pick1, PicksAndBansS7.Team2Pick2, PicksAndBansS7.Team2Pick3, PicksAndBansS7.Team2Pick4, PicksAndBansS7.Team2Pick5, PicksAndBansS7.Team1, PicksAndBansS7.Team2, PicksAndBansS7.Team1PicksByRoleOrder, PicksAndBansS7.Team2PicksByRoleOrder, MatchScheduleGame.Blue, MatchScheduleGame.Red, MatchScheduleGame.Winner, ScoreboardGames.Tournament, ScoreboardGames.Team1, ScoreboardGames.Team2, ScoreboardGames.Gamelength, ScoreboardGames.DateTime_UTC, ScoreboardGames.WinTeam, ScoreboardGames.LossTeam',
                                where = 'ScoreboardGames.Tournament="{}"'.format(tournament),
                                join_on = 'PicksAndBansS7.GameID_Wiki = MatchScheduleGame.GameID_Wiki, MatchScheduleGame.ScoreboardID_Wiki = ScoreboardGames.ScoreboardID_Wiki'
                                )

    except TypeError:
        print >> sys.stderr, 'Tournament Could not be found'
        print >> sys.stderr, 'Please Pick another Tournament'
        sys.exit(1)
    games = []
    for rows in statsQuery['cargoquery']:
        statsQuery_dict = {}
        for keys in rows['title'].keys():
            statsQuery_dict.update({keys:rows['title'][keys]})
        games.append(statsQuery_dict)
    games_df = pd.DataFrame(games)
    games_df = games_df.melt(id_vars=games_df.columns.difference(['Team1Ban1', 'Team1Ban2', 'Team1Ban3', 'Team1Ban4', 'Team1Ban5','Team1Pick1', 'Team1Pick2', 'Team1Pick3', 'Team1Pick4', 'Team1Pick5','Team2Ban1', 'Team2Ban2', 'Team2Ban3', 'Team2Ban4', 'Team2Ban5','Team2Pick1', 'Team2Pick2', 'Team2Pick3', 'Team2Pick4', 'Team2Pick5']), 
        value_vars=['Team1Ban1', 'Team1Ban2', 'Team1Ban3', 'Team1Ban4', 'Team1Ban5','Team1Pick1', 'Team1Pick2', 'Team1Pick3', 'Team1Pick4', 'Team1Pick5','Team2Ban1', 'Team2Ban2', 'Team2Ban3', 'Team2Ban4', 'Team2Ban5','Team2Pick1', 'Team2Pick2','Team2Pick3', 'Team2Pick4', 'Team2Pick5'],
        var_name='Picks',
        value_name='Champions')
    games_df = games_df.melt(id_vars=games_df.columns.difference(['Team1Role1','Team1Role2','Team1Role3','Team1Role4','Team1Role5','Team2Role1','Team2Role2','Team2Role3','Team2Role4','Team2Role5']), 
    value_vars=['Team1Role1','Team1Role2','Team1Role3','Team1Role4','Team1Role5','Team2Role1','Team2Role2','Team2Role3','Team2Role4','Team2Role5'],
    var_name= 'Role', 
    value_name='Position')
    games_df['Role'] = games_df['Role'].str.replace('Role','Pick', regex=False)
    games_df['Column'] = np.where(games_df['Role']==games_df['Picks'], 'True', None)
    games_df = games_df.dropna().drop(columns = ['Column'])
    return games_df

    
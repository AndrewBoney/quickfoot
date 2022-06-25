import pandas as pd
import numpy as np

import os

def read_gw(year, gw):
  return pd.read_csv(f"https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/{year}/gws/gw{gw}.csv")

def read_fixtures(year):
  fix = pd.read_csv(f"https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/{year}/fixtures.csv")
  fix["year"] = year
  return fix

def read_teams(year):
  return pd.read_csv(f"https://raw.githubusercontent.com/vaastav/Fantasy-Premier-League/master/data/{year}/teams.csv")

def download_year_gws(years, data_loc):
    gws = np.arange(1, 38+1)
    
    # lazy for loop because I'm lazy
    for y in years:
        print(f"Running year {y}")
        os.makedirs(f"{data_loc}\{y}", exist_ok = True)
        for gw in gws:
            a = []
            try:
                gw_data = read_gw(y, gw)
                gw_data["year"] = y
                
                gw_data.to_parquet(f"{data_loc}/{y}/gw_{gw}.parquet")
                a.append(gw_data)
            except:
                print(f"skipping: year {y}, gw {gw}. Please check!")
          
def download_teams(years, data_loc):
    for y in years:
        os.makedirs(f"{data_loc}/{y}", exist_ok = True)
        
        try:
            teams = read_teams(y)
            teams["year"] = y
            teams.to_parquet(f"{data_loc}/{y}/teams.parquet")
        
        except:
            print(f"skipping: year {y}. Please check!")
            
def download_fixtures(years, data_loc):
    for y in years:
        os.makedirs(f"{data_loc}/{y}", exist_ok = True)
        
        try:
            fixtures = read_fixtures(y)
            fixtures["year"] = y
            fixtures.to_parquet(f"{data_loc}/{y}/fixtures.parquet")
        
        except:
            print(f"skipping: year {y}. Please check!")
        
def load_year_gws(years, data_loc):
    gws = np.arange(1, 38+1)
    
    # lazy for loop because I'm lazy
    for y in years:
        for gw in gws:
            a = []
            try:
                gw_data = read_gw(y, gw)
                
                gw_data.to_parquet(f"{data_loc}/{y}/gw_{gw}.parquet")
                a.append(gw_data)
            except:
                print(f"skipping: year {y}, gw {gw}. Please check!")        
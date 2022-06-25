import pandas as pd
import numpy as np

def clean_gws(gws_df):
  # Some GK miscoded as GKP. Changing this manually
  gws_df = gws_df.copy()
  gws_df.loc[gws_df["position"] == "GKP", "position"] = "GK"
  gws_df.rename({"opponent_team":"team_against"},axis=1,inplace=True)

  return gws_df.sort_values(["year", "team", "name", "round"]).reset_index(drop=True)

def clean_fixtures(fixtures
                   # , teams
                   ):
  """
  # team file is for names. annoyingly fixtures uses team id but players uses 
  # team name, so we need to do this for merging. 

  fixtures = fixtures.copy()
  fixtures.drop(["team_a_name", "team_h_name"],axis=1,errors="ignore",inplace=True)

  for i in ["team_a", "team_h"]:
    _team = teams[["id", "name"]].rename({"id": i, "name": f"{i}_name"},axis=1)

    fixtures = fixtures.merge(_team, 
                  how = "left",
                  on = i)
  """

  fixtures_home = fixtures.rename({"team_h":"team", "team_h_score":"scored", "team_h_difficulty":"difficulty_against", 
                  "team_a": "team_against","team_a_score":"conceded", "team_a_difficulty":"difficulty"}, axis=1)
  
  fixtures_home = fixtures_home[["year","id",'kickoff_time',"team","team_against","scored", 
                                 "conceded", "difficulty", "difficulty_against"]]

  fixtures_home["home"] = True

  fixtures_away = fixtures_home.rename({"team_against":"team", "team":"team_against", 
                                        "conceded":"scored", "scored":"conceded", 
                                        "difficulty":"difficulty_against", 
                                        "difficulty_against":"difficulty"},axis=1)
  
  fixtures_away["home"] = False

  return pd.concat([fixtures_home, fixtures_away]).sort_values(["year", "team", "id"]).reset_index(drop = True)


def get_match_features(clean_fixtures, 
                       lag_cols = ["scored","conceded","difficulty_against","home"],
                       keep_cols = ["difficulty"],
                       n_lags = 3):
  clean_fixtures = clean_fixtures.copy()
  clean_fixtures["home"] = clean_fixtures["home"].astype(np.int64)

  for i in range(1, n_lags+1):
    nc = [f"_{c}_{i}" for c in lag_cols]
    clean_fixtures[nc] = clean_fixtures.groupby(["year", "team"])[lag_cols].shift(i)

  cols = clean_fixtures.columns
  keep = ["year","id","team","team_against"] + keep_cols + list(cols[cols.str.startswith("_")]) 

  return clean_fixtures[keep] 

def get_player_features(player_data,
                        lag_cols = ["goals_scored","assists","bonus",
                                    "bps","clean_sheets","minutes","ict_index"],
                        #"influence","creativity","threat","ict_index",
                        keep_cols = ["position","transfers_in","transfers_out",
                                     "value"],
                        n_lags = 3):

  player_data = player_data.copy()

  for i in range(1, n_lags+1):
    nc = [f"_{c}_{i}" for c in lag_cols]
    player_data[nc] = player_data.groupby(["year", "team", "name"])[lag_cols].shift(i)
  
  player_data = pd.concat([
      player_data,
      get_cat_y(player_data)  
    ], axis=1)
  
  cols = player_data.columns
  
  id_ = ["year","team","team_against","name","round","fixture"]
  keep = id_ + keep_cols + list(cols[cols.str.startswith("_")]) 

  return player_data[keep + ["total_points"]]


def get_cat_y(features):
    """
    Make Y features:
        - Minutes (0, <60, >=60)
        - Goals Scored (0, 1, 2, 3+)
        - Assists (0, 1, 2, 3+)
        - Goals Conceced (0, 1, 2, 3, 4, 5+)
        - Shots Saved (0-3, 3-6, 6+)
        - Pens Saved (0, 1+)
        - Pens Missed (0, 1+)
        - Yellow Card (0, 1)
        - Red Card (0, 1)
        - Own Goals (0, 1+)

    Parameters
    ----------
    features : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    
    features = features.copy()

    features["_cat_minutes"] = np.select(
        [features["minutes"] == 0, 
         (features["minutes"] > 0) & (features["minutes"] < 60), 
         features["minutes"] >= 60],
        ["0", "<60", ">=60"], 
        np.nan)

    features["_cat_goals_scored"] = np.where(features["goals_scored"] >= 3, 
                                             "3+", 
                                             features["goals_scored"].astype(str))
    
    features["_cat_assists"] = np.where(features["assists"] >= 3, 
                                             "3+", 
                                             features["assists"].astype(str))
    
    features["_cat_goals_conceded"] = np.where(features["goals_conceded"] >= 3, 
                                             "3+", 
                                             features["goals_conceded"].astype(str))

    features["_cat_saves"] = np.select(
        [(features["saves"] >= 0) & (features["saves"] < 3),
         (features["saves"] >= 3) & (features["saves"] < 6),
         features["saves"] >= 6],
        ["<3", "3-<6", "6+"], 
        np.nan)
    
    features["_cat_pens_saved"] = np.where(features["penalties_saved"] >= 1, "1+", "0")
    features["_cat_pens_missed"] = np.where(features["penalties_missed"] >= 1, "1+", "0")
    features["_cat_own_goals"] = np.where(features["own_goals"] >= 1, "1+", "0")
    
    cols = features.columns[features.columns.str.startswith("_cat")]
    
    return features[list(cols) + ["yellow_cards", "red_cards"]]


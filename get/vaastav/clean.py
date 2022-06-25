import pandas as pd

def clean_gws(gws_df):
  # Some GK miscoded as GKP. Changing this manually
  gws_df = gws_df.copy()
  gws_df.loc[gws_df["position"] == "GKP", "position"] = "GK"
  gws_df.rename({"opponent_team":"team_against"},axis=1,inplace=True)

  return gws_df[["year", "team", "team_against", "round", "name", "position", 
           "total_points","fixture", "assists","bonus", "bps", "clean_sheets", 
           "ict_index", "influence", "creativity", 
           "threat", "transfers_in", "transfers_out", "value","goals_scored", 
           "minutes"]].sort_values(["year", "team", "name", "round"]).reset_index(drop=True)

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
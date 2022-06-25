import os

from get.vaastav.imp import *

os.makedirs("data")
os.makedirs("data/vaastav")
os.makedirs("data/vaastav/players")
os.makedirs("data/vaastav/fixtures")
os.makedirs("data/vaastav/teams")

download_year_gws(["2021-22", "2020-21", "2019-20"],
               "data/vaastav/players")

download_teams(["2021-22", "2020-21", "2019-20"],
               "data/vaastav/teams")

download_fixtures(["2021-22", "2020-21", "2019-20"],
               "data/vaastav/fixtures")


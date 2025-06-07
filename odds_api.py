import random

# Simulated spread/total lines for matchups
team_odds = {
    ("LAL", "BOS"): {"spread": -4.5, "total": 227.5},
    ("GSW", "MIA"): {"spread": 2.0, "total": 223.0},
    ("NYK", "CHI"): {"spread": -1.5, "total": 220.0},
    ("MIL", "PHX"): {"spread": -3.5, "total": 230.5},
}

# Simulated player prop lines
player_props = {
    "LeBron James": {"points": 26.5, "rebounds": 7.5, "assists": 7.5},
    "Kevin Durant": {"points": 27.5, "rebounds": 6.5, "assists": 5.5},
    "Steph Curry": {"points": 28.0, "rebounds": 4.5, "assists": 6.5},
    "Jayson Tatum": {"points": 26.5, "rebounds": 8.0, "assists": 4.5},
    "Luka Doncic": {"points": 29.5, "rebounds": 8.5, "assists": 8.5},
    "Tyrese Haliburton": {"points": 21.5, "rebounds": 3.5, "assists": 10.0},
    "Giannis Antetokounmpo": {"points": 30.5, "rebounds": 11.0, "assists": 5.5},
    "Trae Young": {"points": 24.5, "rebounds": 3.0, "assists": 9.5},
}

def get_team_odds(home_team, away_team):
    return team_odds.get((home_team, away_team), {
        "spread": round(random.uniform(-6, 6), 1),
        "total": round(random.uniform(215, 235), 1)
    })

def get_player_prop(player_name, stat):
    return player_props.get(player_name, {}).get(stat, round(random.uniform(5, 30), 1))

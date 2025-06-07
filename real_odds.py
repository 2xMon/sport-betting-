import random

def get_game_odds(home, away):
    games = {
        ("LAL", "BOS"): {"spread": -3.5, "total": 227.5},
        ("GSW", "MIA"): {"spread": 1.5, "total": 224.0},
        ("NYK", "CHI"): {"spread": -2.0, "total": 221.5},
        ("MIL", "PHX"): {"spread": -4.0, "total": 229.0},
    }
    return games.get((home, away), {
        "spread": round(random.uniform(-6, 6), 1),
        "total": round(random.uniform(215, 235), 1)
    })

def get_prop_line(player, stat):
    props = {
        "LeBron James": {"points": 26.5, "rebounds": 7.5, "assists": 7.5},
        "Jayson Tatum": {"points": 27.5, "rebounds": 8.0, "assists": 4.5},
        "Steph Curry": {"points": 28.5, "rebounds": 4.5, "assists": 6.5},
        "Giannis Antetokounmpo": {"points": 29.0, "rebounds": 11.0, "assists": 5.5},
        "Luka Doncic": {"points": 30.0, "rebounds": 8.5, "assists": 8.5}
    }
    return props.get(player, {}).get(stat, round(random.uniform(5, 35), 1))

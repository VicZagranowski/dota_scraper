start_url = 'https://api.opendota.com/api/heroStats?'
matchups_url = 'https://api.opendota.com/api/heroes/{}/matchups?'


def extract_top_hereos(data: list[dict]):
    x = sorted(
        data,
        key=lambda k: k['turbo_wins'] * 100 / k['turbo_picks']
    )
    return x[0:3]


def extract_lowest_winrate(data: list[dict]):
    x = sorted(
        data,
        key=lambda k: k['wins']*100/k['games_played'],
        reverse=True
    )
    return x[0:10]



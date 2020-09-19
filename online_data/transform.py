import pandas as pd
from football.league import get_dict_followed_country_and_competition


def get_matches_from_followed_competitions(
        df_fixtures,
        df_leagues,
        map_country_competitions=get_dict_followed_country_and_competition()):
    df_followed_leagues = df_leagues.copy()
    df_followed_leagues['followed'] = df_followed_leagues.apply(
        lambda r: r['country'] in map_country_competitions.keys() and
        r['name'] in map_country_competitions[r['country']], axis=1)
    df_followed_leagues = df_followed_leagues.astype({'league_id': 'int32'})
    df_fixtures = df_fixtures.astype({'league_id': 'int32'})
    ids = df_followed_leagues[df_followed_leagues['followed']
                              ]['league_id'].values
    df_fixtures_from_leagues = df_fixtures[df_fixtures['league_id'].isin(ids)]
    df_fixtures_from_leagues.set_index('league_id', inplace=True)
    df_followed_leagues = df_followed_leagues[df_followed_leagues['followed']]
    df_followed_leagues.set_index('league_id', inplace=True)
    df_fixtures_from_leagues = df_fixtures_from_leagues.join(
        df_followed_leagues[['country', 'name']]).reset_index()
    return df_fixtures_from_leagues


def transform_fixture_api(fixture_api, league_api):
    df_leagues = pd.json_normalize(league_api['api']['leagues'])
    df_fixtures = pd.DataFrame(
        [x for _, x in fixture_api['api']['fixtures'].items()])
    df_fixtures = get_matches_from_followed_competitions(
        df_fixtures, df_leagues)
    return df_fixtures

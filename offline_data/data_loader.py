import pandas as pd
import os


class DataLoader(object):
    """
    Class used to generate raw data used to train and evaluate performance of predictor
    """
    LEAGUE_IDS = {
        0: 'PremierLeague',
        1: 'Championship'
    }

    LEGEND = {
        "Div": "League Division",
        "Date": "Match Date (dd/mm/yy)",
        "Time": "Time of match kick off",
        "HomeTeam": "Home Team",
        "AwayTeam": "Away Team",
        "FTHG": "Full Time Home Team Goals",
        "HG": "Full Time Home Team Goals",
        "FTAG": "Full Time Away Team Goals",
        "AG": "Full Time Away Team Goals",
        "FTR": "Full Time Result",
        "Res": "Full Time Result",
        "HTHG": "Half Time Home Team Goals",
        "HTAG": "Half Time Away Team Goals",
        "HTR": "Half Time Result",
        "Attendance": "Crowd Attendance",
        "Referee": "Match Referee",
        "HS": "Home Team Shots",
        "AS": "Away Team Shots",
        "HST": "Home Team Shots on Target",
        "AST": "Away Team Shots on Target",
        "HHW": "Home Team Hit Woodwork",
        "AHW": "Away Team Hit Woodwork",
        "HC": "Home Team Corners",
        "AC": "Away Team Corners",
        "HF": "Home Team Fouls Committed",
        "AF": "Away Team Fouls Committed",
        "HFKC": "Home Team Free Kicks Conceded",
        "AFKC": "Away Team Free Kicks Conceded",
        "HO": "Home Team Offsides",
        "AO": "Away Team Offsides",
        "HY": "Home Team Yellow Cards",
        "AY": "Away Team Yellow Cards",
        "HR": "Home Team Red Cards",
        "AR": "Away Team Red Cards",
    }

    def __init__(self, download_data_dir, league_ids):
        self.data_dir = download_data_dir
        self.leagues = league_ids

    def extract_and_store_data(self, output_dir):
        raw_data_files = self._get_list_csv_files_in_dir()
        for league_id in self.leagues:
            if league_id in DataLoader.LEAGUE_IDS.keys():
                output_data = os.path.join(output_dir, DataLoader.LEAGUE_IDS[league_id] + '.csv')
                league_data_files = list(filter(lambda file: file.startswith(f'E{league_id}'), raw_data_files))
                dfs = list(map(lambda file: pd.read_csv(os.path.join(self.data_dir, file), encoding="ISO-8859-1"),
                               league_data_files))
                keys = DataLoader.LEGEND.keys()
                dfs = [df.loc[:, df.columns.isin(keys)] for df in dfs]
                pd.concat(dfs, ignore_index=True).to_csv(output_data)
            else:
                print(f'{league_id} is not supported by class')

    def _get_list_csv_files_in_dir(self):
        list_files = os.listdir(self.data_dir)
        extension = 'csv'
        return list(filter(lambda file: file.endswith(extension), list_files))

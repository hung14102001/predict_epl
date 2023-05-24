import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
}
standings_url = "https://fbref.com/en/comps/9/Premier-League-Stats"
response = requests.get(standings_url, headers=headers)
print(response.status_code)
soup = BeautifulSoup(response.text,"html.parser")
standings_table = soup.find('table',id="results2022-202391_overall")


links = standings_table.find_all('a')
links = [l.get("href") for l in links]
links = [l for l in links if '/squads/' in l]
team_urls = [f"https://fbref.com{l}" for l in links]
played_matches = []
predict_matches = []
for team_url in team_urls:

    team_data = requests.get(team_url)

    team_name = team_url.split("/")[-1].replace("-Stats", "").replace("-", " ")
    soup = BeautifulSoup(team_data.text,"html.parser")
    table_match_team_data = soup.find('table',id="matchlogs_for")

    match_team_data = pd.read_html(str(table_match_team_data))[0]
    predict_data = pd.read_html(str(table_match_team_data))[0]

    match_team_data = match_team_data[match_team_data["Comp"] == "Premier League"]
    predict_data = predict_data[predict_data["Comp"] == "Premier League"]
    fill_na_list = ['xG',	'xGA',	'Poss']

    for l in fill_na_list:
        match_team_data[l] = match_team_data.groupby("Team")[l].transform(lambda x: x.fillna(x.mean()))
        predict_data[l] = predict_data.groupby("Team")[l].transform(lambda x: x.fillna(x.mean()))

    played_match = match_team_data[match_team_data["Match Report"] == "Match Report"]
    predict_match = predict_data[predict_data["Match Report"] == "Head-to-Head"]
    played_match["Team"] = team_name
    predict_match["Team"] = team_name

    played_matches.append(played_match)
    predict_matches.append(predict_match)
    time.sleep(1)

match_df = pd.concat(played_matches)
match_df.columns = [c.lower() for c in match_df.columns]

predict_match_df = pd.concat(predict_matches)
predict_match_df.columns = [c.lower() for c in predict_match_df.columns]

class MissingDict(dict):
    __missing__ = lambda self, key: key

map_values = {"Brighton and Hove Albion": "Brighton", "Manchester United": "Manchester Utd", "Newcastle United": "Newcastle Utd", "Nottingham Forest":"Nott'ham Forest", "Tottenham Hotspur": "Tottenham", "West Ham United": "West Ham", "Wolverhampton Wanderers": "Wolves"} 
mapping = MissingDict(**map_values)
match_df["team"] = match_df["team"].map(mapping)
predict_match_df["team"] = predict_match_df["team"].map(mapping)

del_list = ["comp", "attendance", "captain", "formation", "referee", "notes"]
for l in del_list:
    del match_df[l]
    del predict_match_df[l]
match_df.to_csv("final_all_matches_played.csv")
predict_match_df.to_csv("final_predict_matches.csv")



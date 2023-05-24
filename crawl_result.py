import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
# headers = {
# 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
# }
# standings_url = "https://fbref.com/en/comps/9/Premier-League-Stats"

# response = requests.get(standings_url, headers=headers)
# print(response.status_code)
# soup = BeautifulSoup(response.text,"html.parser")
# standings_table = soup.find('table',id="results2022-202391_overall")


# links = standings_table.find_all('a')
# links = [l.get("href") for l in links]
# links = [l for l in links if '/squads/' in l]
# team_urls = [f"https://fbref.com{l}" for l in links]
# predicted_matches = []
# for team_url in team_urls:
#     time.sleep(1)
#     team_data = requests.get(team_url)

#     team_name = team_url.split("/")[-1].replace("-Stats", "").replace("-", " ")
#     soup = BeautifulSoup(team_data.text,"html.parser")
#     table_match_team_data = soup.find('table',id="matchlogs_for")

#     match_team_data = pd.read_html(str(table_match_team_data))[0]

#     match_team_data = match_team_data[match_team_data["Comp"] == "Premier League"]
#     predicted_match = match_team_data[match_team_data['Date'] >'2023-05-10']
#     predicted_match = predicted_match[predicted_match["Match Report"] == "Match Report"]
#     predicted_match['team'] = team_name


#     predicted_matches.append(predicted_match)
#     time.sleep(1)

# predict_match_df = pd.concat(predicted_matches)
# predict_match_df.columns = [c.lower() for c in predict_match_df.columns]


# predict_match_df['result'] = predict_match_df['result'].fillna('unplayed match')
# predict_match_df['gf'] = predict_match_df['gf'].fillna('unplayed match')
# predict_match_df['ga'] = predict_match_df['ga'].fillna('unplayed match')



# predict_match_df.to_csv("result_10_05_22_05.csv")
# data_frame = pd.read_csv('result_unplayedWDL.csv', index_col = False)
# data_frame = data_frame[data_frame['date'] <'2023-05-22']
# predict_match_df["result"].replace({"W": 3, "D": 1, "L": 0})

# data_frame['result'].fillna(pd.Series(predict_match_df['result'].values), inplace=True)
# data_frame['gf'].fillna(pd.Series(predict_match_df['gf'].values), inplace=True)
# data_frame['ga'].fillna(pd.Series(predict_match_df['ga'].values), inplace=True)


# data_frame.to_csv("2205_predict_matchesWDL.csv", index = False)

df = pd.read_csv("result.csv")
df["result"].replace({"W": 3, "D": 1, "L": 0}, inplace=True)
df.to_csv("results.csv", index=False)
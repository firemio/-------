import sys
import time
import requests
from bs4 import BeautifulSoup
import yaml
import json

# Pythonの最大再帰深度を増やす
sys.setrecursionlimit(3000)  # 例として3000に設定

def fetch_boat_race_data(jcd):
    url = f"https://www.boatrace.jp/owpc/pc/data/stadium?jcd={jcd}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # ボートレース場の名前を取得
    race_place_name = soup.find('h2').get_text(strip=True)
    table = str.maketrans({
    '\u3000': '',
    ' ': '',
    '\t': '',
    })
    race_place_name = race_place_name.translate(table)
    race_place_name.replace('ボートレース場', '')


    # コース別入着率＆決まり手のデータを抽出
    course_table = soup.find_all('table')[0]
    rows = course_table.find_all('tr')

    # データを整形
    data = {race_place_name: {"最近3ヶ月のデータ": {"コース別入着率＆決まり手": {}}}}
    for i, row in enumerate(rows[1:]):  # ヘッダー行をスキップ
        columns = row.find_all('td')
        if columns:
            course = f"{i}コース"
            data[race_place_name]["最近3ヶ月のデータ"]["コース別入着率＆決まり手"][course] = {
                "1着": columns[1].get_text(strip=True)+'%',
                "2着": columns[2].get_text(strip=True)+'%',
                "3着": columns[3].get_text(strip=True)+'%',
                "4着": columns[4].get_text(strip=True)+'%',
                "5着": columns[5].get_text(strip=True)+'%',
                "6着": columns[6].get_text(strip=True)+'%',
                "コース別決まり手": {
                    "逃げ": columns[7].get_text(strip=True)+'%',
                    "捲り": columns[8].get_text(strip=True)+'%',
                    "差し": columns[9].get_text(strip=True)+'%',
                    "捲り差し": columns[10].get_text(strip=True)+'%',
                    "抜き": columns[11].get_text(strip=True)+'%',
                    "恵まれ": columns[12].get_text(strip=True)+'%',
                }
            }




    # 季節別データの追加
    data[race_place_name]["季節別データ"] = {}

    # 各季節のデータを抽出
    seasons = ["春季", "夏季", "秋季", "冬季"]
    for i, season in enumerate(seasons, start=2):  # 3番目のテーブルから開始
        season_table = soup.find_all('table')[i]
        season_rows = season_table.find_all('tr')
        season_data = {}
        for j, row in enumerate(season_rows[1:]):  # ヘッダー行をスキップ
            columns = row.find_all('td')
            if columns:
                course = f"{j+1}コース"
                season_data[course] = {
                    "1着": columns[1].get_text(strip=True)+'%',
                    "2着": columns[2].get_text(strip=True)+'%',
                    "3着": columns[2].get_text(strip=True)+'%',
                    "4着": columns[2].get_text(strip=True)+'%',
                    "5着": columns[2].get_text(strip=True)+'%',
                    "6着": columns[2].get_text(strip=True)+'%',
                }
        data[race_place_name]["季節別データ"][season] = season_data

    return data


    return data

def save_to_yaml(data, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        yaml.dump(data, file, allow_unicode=True)

def save_to_json(data, filename):
    with open(f'{filename}.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


all_data = []

for i in range(1, 25):  #01～24まで
    jcd = str(i).zfill(2)  # This will convert the number to a string and pad with zeros
    print(jcd)
    data = fetch_boat_race_data(jcd)
    # save_to_yaml(data, f'stadium{jcd}.yaml')
    time.sleep(3)
    all_data.append(data)

# save_to_yaml(all_data, f'stadium_all.yaml')
save_to_json(all_data, f'stadium_all')


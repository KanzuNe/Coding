import requests
from bs4 import BeautifulSoup
import re
import csv
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0'}
url = "https://edurank.org/uni/posts-and-telecommunications-institute-of-technology/"
resp = requests.get(url, headers=headers)
if resp.status_code != 200:
    print(f"Failed to fetch {url}, status code: {resp.status_code}")
    exit(1)

soup = BeautifulSoup(resp.text, 'html.parser')

university_name = "Posts and Telecommunications Institute of Technology"
vietnam_rank = ""
asia_rank = ""
world_rank = ""
city = "Hanoi"

# Get ranks
ranks = soup.find_all('div', class_='uni-card__rank')
for r in ranks:
    span = r.find('span', class_='text-fat')
    if span:
        val = span.text.strip()
        if 'Vietnam' in r.text:
            vietnam_rank = val
        elif 'Asia' in r.text:
            asia_rank = val
        elif 'World' in r.text:
            world_rank = val

acceptance_rate = ""
enrollment = ""
founded = ""

info_dl = soup.find('dl', class_='uni-card__info-list')
if info_dl:
    for div in info_dl.find_all('div'):
        dt = div.find('dt')
        dd = div.find('dd')
        if dt and dd:
            key = dt.text.strip()
            value = dd.text.strip()
            if 'Acceptance' in key:
                acceptance_rate = value.replace('%', '')
            elif 'Enrollment' in key:
                enrollment = value.replace(',', '')
            elif 'Founded' in key:
                founded = value

ai_pubs = ""
ai_cits = ""
for th in soup.find_all('th', scope='row'):
    if 'Artificial Intelligence' in th.text:
        tr = th.parent
        td = tr.find('td')
        if td:
            spans = td.find_all('span')
            if len(spans) >= 2:
                ai_pubs = spans[0].text.strip().replace(',', '')
                ai_cits = spans[1].text.strip().replace('/', '').replace(',', '').strip()

tuition = ""
tbl = soup.find(string=re.compile('Tuition Cost'))
if tbl:
    parent_table = tbl.find_parent('table')
    if parent_table:
        for tr in parent_table.find_all('tr'):
            tds = tr.find_all('td')
            if len(tds) >= 2 and 'Bachelor' in tds[0].text:
                tuition = tds[1].text.strip().replace(',', '')
                break
        if not tuition:
            for tr in parent_table.find_all('tr'):
                tds = tr.find_all('td')
                if len(tds) >= 2:
                    tuition = tds[1].text.strip().replace(',', '')
                    break

print({
    "University_Name": university_name,
    "Vietnam_Rank": vietnam_rank,
    "Asia_Rank": asia_rank,
    "World_Rank": world_rank,
    "City": city,
    "Acceptance_Rate": acceptance_rate,
    "Enrollment": enrollment,
    "Founded": founded,
    "AI_Publications": ai_pubs,
    "AI_Citations": ai_cits,
    "Tuition_VND": tuition
})

df = pd.DataFrame([{
    "University_Name": university_name,
    "Vietnam_Rank": vietnam_rank,
    "Asia_Rank": asia_rank,
    "World_Rank": world_rank,
    "City": city,
    "Acceptance_Rate": acceptance_rate,
    "Enrollment": enrollment,
    "Founded": founded,
    "AI_Publications": ai_pubs,
    "AI_Citations": ai_cits,
    "Tuition_VND": tuition
}])
df_edu = pd.read_csv('edurank_ai_rankings.csv')
# Append if not exists
if university_name not in df_edu['University_Name'].values:
    df_edu = pd.concat([df_edu, df], ignore_index=True)
    df_edu.to_csv('edurank_ai_rankings.csv', index=False)
    print("Added to edurank_ai_rankings.csv")


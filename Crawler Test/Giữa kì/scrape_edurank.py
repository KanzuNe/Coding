import requests
from bs4 import BeautifulSoup
import csv

def scrape_edurank():
    url = 'https://edurank.org/cs/ai/vn/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return
        
    soup = BeautifulSoup(response.text, 'html.parser')
    
    universities_data = []
    
    for h2 in soup.find_all('h2'):
        text = h2.text.strip()
        
        if '. ' in text and text.split('. ')[0].isdigit():
            vietnam_rank = int(text.split('. ')[0])
            university_name = text.split('. ', 1)[1]
            
            container = h2.find_parent('div', class_='block-cont') or h2.parent
            
            city = ""
            geo_div = container.find('div', class_='uni-card__geo')
            if geo_div:
                links = geo_div.find_all('a')
                if len(links) >= 2:
                    city = links[1].text.strip()
                
            asia_rank = ""
            ranks_div = container.find_all('div', class_='uni-card__rank')
            for rank_div in ranks_div:
                if 'Asia' in rank_div.text:
                    span = rank_div.find('span', class_='text-fat')
                    if span:
                        asia_rank_text = span.text.strip()
                        if asia_rank_text.isdigit():
                            asia_rank = int(asia_rank_text)
                        else:
                            asia_rank = asia_rank_text
            
            universities_data.append({
                "University_Name": university_name,
                "Vietnam_Rank": vietnam_rank,
                "Asia_Rank": asia_rank,
                "City": city
            })

    csv_file = 'edurank_ai_rankings.csv'
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["University_Name", "Vietnam_Rank", "Asia_Rank", "City"])
        writer.writeheader()
        writer.writerows(universities_data)

if __name__ == "__main__":
    scrape_edurank()

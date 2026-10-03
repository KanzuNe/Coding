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
            world_rank = ""
            ranks_div = container.find_all('div', class_='uni-card__rank')
            for rank_div in ranks_div:
                span = rank_div.find('span', class_='text-fat')
                if span:
                    val = span.text.strip()
                    val = int(val) if val.isdigit() else val
                    if 'Asia' in rank_div.text:
                        asia_rank = val
                    elif 'World' in rank_div.text:
                        world_rank = val
            
            # Khai thác thêm dữ liệu (Acceptance Rate, Enrollment, Founded)
            acceptance_rate = ""
            enrollment = ""
            founded = ""
            
            info_dl = container.find('dl', class_='uni-card__info-list')
            if info_dl:
                for div in info_dl.find_all('div'):
                    dt = div.find('dt')
                    dd = div.find('dd')
                    if dt and dd:
                        key = dt.text.strip()
                        value = dd.text.strip()
                        if 'Acceptance' in key:
                            acceptance_rate = value.replace('%', '') # Bỏ dấu % để dễ tính toán sau này
                        elif 'Enrollment' in key:
                            enrollment = value.replace(',', '') # Bỏ dấu phẩy
                        elif 'Founded' in key:
                            founded = value
            
            universities_data.append({
                "University_Name": university_name,
                "Vietnam_Rank": vietnam_rank,
                "Asia_Rank": asia_rank,
                "World_Rank": world_rank,
                "City": city,
                "Acceptance_Rate": acceptance_rate,
                "Enrollment": enrollment,
                "Founded": founded
            })

    csv_file = 'edurank_ai_rankings.csv'
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ["University_Name", "Vietnam_Rank", "Asia_Rank", "World_Rank", "City", "Acceptance_Rate", "Enrollment", "Founded"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(universities_data)
        
    print(f"Scraped {len(universities_data)} universities to {csv_file}")

if __name__ == "__main__":
    scrape_edurank()

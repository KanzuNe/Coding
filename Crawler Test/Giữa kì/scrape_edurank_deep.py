import requests
from bs4 import BeautifulSoup
import csv
import time
import re

def scrape_edurank_deep():
    base_url = 'https://edurank.org'
    start_url = f'{base_url}/cs/ai/vn/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    print(f"Bắt đầu crawl danh sách trường ĐH từ: {start_url}")
    response = requests.get(start_url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch {start_url}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    universities_data = []

    # Tìm danh sách các trường
    containers = soup.find_all('div', class_='block-cont pt-4 mb-4')
    print(f"Đã tìm thấy {len(containers)} trường ĐH có ngành AI. Đang trích xuất dữ liệu sâu...")

    for i, container in enumerate(containers):
        # 1. Trích xuất dữ liệu cơ bản (Basic Info)
        name_tag = container.find('h2').find('a')
        university_name = name_tag.text.split('. ', 1)[-1].strip()
        uni_link = name_tag['href']
        if not uni_link.startswith('http'):
            uni_link = base_url + uni_link
        
        geo_div = container.find('div', class_='uni-card__geo')
        city = geo_div.find_all('a')[-1].text.strip() if geo_div else ""
        
        ranks = container.find_all('div', class_='uni-card__rank')
        asia_rank = ""
        world_rank = ""
        vietnam_rank = str(i + 1)
        for r in ranks:
            span = r.find('span', class_='text-fat')
            if span:
                val = span.text.strip()
                if 'Asia' in r.text:
                    asia_rank = val
                elif 'World' in r.text:
                    world_rank = val

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
                        acceptance_rate = value.replace('%', '')
                    elif 'Enrollment' in key:
                        enrollment = value.replace(',', '')
                    elif 'Founded' in key:
                        founded = value

        # 2. Truy cập vào trang chi tiết của trường (Deep Crawl)
        print(f"[{i+1}/{len(containers)}] Đang crawl chi tiết: {university_name}")
        ai_pubs = ""
        ai_cits = ""
        tuition = ""
        
        try:
            detail_resp = requests.get(uni_link, headers=headers)
            detail_soup = BeautifulSoup(detail_resp.text, 'html.parser')
            
            # Lấy AI Pubs & Citations
            for th in detail_soup.find_all('th', scope='row'):
                if 'Artificial Intelligence' in th.text:
                    tr = th.parent
                    td = tr.find('td')
                    if td:
                        spans = td.find_all('span')
                        if len(spans) >= 2:
                            ai_pubs = spans[0].text.strip().replace(',', '')
                            ai_cits = spans[1].text.strip().replace('/', '').replace(',', '').strip()
            
            # Lấy Tuition (Học phí)
            tbl = detail_soup.find(string=re.compile('Tuition Cost'))
            if tbl:
                parent_table = tbl.find_parent('table')
                if parent_table:
                    # Ưu tiên lấy học phí Bachelor
                    for tr in parent_table.find_all('tr'):
                        tds = tr.find_all('td')
                        if len(tds) >= 2 and 'Bachelor' in tds[0].text:
                            tuition = tds[1].text.strip().replace(',', '')
                            break
                    if not tuition:
                        # Lấy dòng đầu tiên nếu không thấy Bachelor
                        for tr in parent_table.find_all('tr'):
                            tds = tr.find_all('td')
                            if len(tds) >= 2:
                                tuition = tds[1].text.strip().replace(',', '')
                                break
                                
            # Giữ thời gian chờ để không bị chặn (Polite crawling)
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Lỗi khi crawl chi tiết {university_name}: {e}")

        universities_data.append({
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

    # 3. Lưu vào CSV
    csv_file = 'edurank_ai_rankings.csv'
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ["University_Name", "Vietnam_Rank", "Asia_Rank", "World_Rank", "City", 
                      "Acceptance_Rate", "Enrollment", "Founded", "AI_Publications", "AI_Citations", "Tuition_VND"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(universities_data)
        
    print(f"\nĐã crawl sâu và xuất dữ liệu {len(universities_data)} trường ra {csv_file}")

if __name__ == "__main__":
    scrape_edurank_deep()

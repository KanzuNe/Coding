import requests
from bs4 import BeautifulSoup
import json

def scrape_hust_edurank():
    url = 'https://edurank.org/cs/ai/vn/'
    # Thêm Header User-Agent để tránh bị block bởi EduRank
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    print("Đang kết nối tới EduRank...")
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Lỗi: Không thể truy cập trang web (Mã lỗi: {response.status_code})")
        return
        
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Biến lưu trữ dữ liệu của HUST
    hust_data = None
    
    # Duyệt qua các thẻ h2 chứa thông tin xếp hạng
    for h2 in soup.find_all('h2'):
        text = h2.text.strip()
        
        # Kiểm tra xem có đúng format "Rank. Tên trường" không
        if '. ' in text and text.split('. ')[0].isdigit():
            # Chú trọng tìm HUST
            if 'Hanoi University of Science and Technology' in text:
                # 1. Trích xuất Hạng Quốc gia và Tên trường
                vietnam_rank = text.split('. ')[0]
                university_name = text.split('. ', 1)[1]
                
                # 2. Tìm container block của trường (thẻ cha chứa h2)
                container = h2.find_parent('div', class_='block-cont') or h2.parent
                
                # 3. Trích xuất Thành phố
                city = "Unknown"
                geo_div = container.find('div', class_='uni-card__geo')
                if geo_div:
                    links = geo_div.find_all('a')
                    if len(links) >= 2:
                        city = links[1].text.strip()
                    
                # 4. Trích xuất Hạng Châu Á
                asia_rank = "Unknown"
                ranks_div = container.find_all('div', class_='uni-card__rank')
                for rank_div in ranks_div:
                    if 'Asia' in rank_div.text:
                        span = rank_div.find('span', class_='text-fat')
                        if span:
                            asia_rank = span.text.strip()
                
                hust_data = {
                    "Tên trường": university_name,
                    "Hạng Quốc gia (VN)": int(vietnam_rank),
                    "Hạng Châu Á (Asia)": int(asia_rank) if asia_rank.isdigit() else asia_rank,
                    "Thành phố": city
                }
                break

    if hust_data:
        print("\n✅ Đã trích xuất thành công dữ liệu của HUST:\n")
        print(json.dumps(hust_data, indent=4, ensure_ascii=False))
    else:
        print("\n❌ Không tìm thấy HUST trong bảng xếp hạng. Có thể web đã thay đổi cấu trúc.")

if __name__ == "__main__":
    scrape_hust_edurank()

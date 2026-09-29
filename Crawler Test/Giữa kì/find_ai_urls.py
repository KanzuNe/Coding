import requests
from bs4 import BeautifulSoup
import time
import urllib.parse

universities = [
    "Đại học Bách khoa Hà Nội",
    "Đại học Công nghệ, ĐHQGHN",
    "Đại học Khoa học Tự nhiên, ĐHQGHN",
    "Đại học Bách khoa, ĐHQG-HCM",
    "Đại học Công nghệ Thông tin, ĐHQG-HCM",
    "Đại học Khoa học Tự nhiên, ĐHQG-HCM",
    "Đại học Bách khoa, ĐH Đà Nẵng",
    "Học viện Công nghệ Bưu chính Viễn thông",
    "Học viện Kỹ thuật Quân sự",
    "Học viện Kỹ thuật Mật mã",
    "Đại học Sư phạm Kỹ thuật TP.HCM",
    "Đại học Công nghiệp Hà Nội",
    "Đại học Công nghiệp TP.HCM",
    "Đại học Giao thông Vận tải",
    "Đại học Thủy lợi",
    "Đại học Xây dựng Hà Nội",
    "Đại học Mỏ - Địa chất",
    "Đại học Mở Hà Nội",
    "Đại học Khoa học và Công nghệ Hà Nội",
    "Đại học Cần Thơ",
    "Đại học Khoa học, ĐH Huế",
    "Đại học Quốc tế, ĐHQG-HCM",
    "Đại học FPT",
    "Đại học Tôn Đức Thắng",
    "Đại học RMIT Việt Nam",
    "Đại học Duy Tân",
    "Đại học Phenikaa",
    "Đại học Văn Lang",
    "Đại học Công nghệ TP.HCM",
    "Đại học Hoa Sen"
]

def search_ddg(query):
    url = "https://html.duckduckgo.com/html/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    data = {"q": query}
    try:
        res = requests.post(url, headers=headers, data=data, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        urls = []
        for a in soup.find_all('a', class_='result__url'):
            href = a.get('href', '').strip()
            # Bỏ qua các URL chứa duckduckgo redirect để lấy URL sạch
            if href.startswith('//duckduckgo.com/l/?'):
                parsed_url = urllib.parse.urlparse(href)
                query_params = urllib.parse.parse_qs(parsed_url.query)
                if 'uddg' in query_params:
                    href = query_params['uddg'][0]
            if href:
                urls.append(href)
            if len(urls) >= 3:
                break
        return urls
    except Exception as e:
        print(f"Lỗi truy vấn: {e}")
        return []

def main():
    results = {}
    print("Bắt đầu tìm kiếm lại bằng bộ cào DuckDuckGo tự viết...")
    
    for uni in universities:
        query = f'"{uni}" tuyển sinh ngành trí tuệ nhân tạo khoa học dữ liệu'
        print(f"Đang tìm kiếm cho: {uni}")
        urls = search_ddg(query)
        results[uni] = urls
        time.sleep(2) # Tránh bị block IP
            
    print("\nĐã tìm kiếm xong, đang xuất ra file markdown...")
    
    with open("ai_program_urls.md", "w", encoding="utf-8") as f:
        f.write("# 🔗 URL Ngành AI / Khoa học dữ liệu của 30 Trường ĐH\n\n")
        f.write("Đây là danh sách được tự động tìm kiếm trên DuckDuckGo. Hãy click vào các đường link này để xem thông tin chi tiết về chương trình đào tạo, chuẩn đầu ra, học phí và đối tác việc làm của từng trường.\n\n")
        for uni, urls in results.items():
            f.write(f"### {uni}\n")
            if urls:
                for url in urls:
                    f.write(f"- {url}\n")
            else:
                f.write("- *(Không tìm thấy kết quả)*\n")
            f.write("\n")
            
    print("Xong! File ai_program_urls.md đã được cập nhật.")

if __name__ == "__main__":
    main()

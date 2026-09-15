import csv
import requests
from bs4 import BeautifulSoup

ten_file = "Nguyen Trung Hieu_B25DCTN035_LAB1.csv"
base_url = "https://quotes.toscrape.com"
url = base_url

danh_sach_quotes = []

while url:
    print(f"Đang cào dữ liệu từ: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    quotes = soup.find_all("div", class_="quote")

    for q in quotes:
        cau_noi = q.find("span", class_="text").text
        tac_gia = q.find("small", class_="author").text
        tags = [t.text for t in q.find_all("a", class_="tag")]
        chuoi_tags = ";".join(tags)
        danh_sach_quotes.append({
            "Quote": cau_noi,
            "Author": tac_gia,
            "Tags": chuoi_tags
        })

    nut_next = soup.find("li", class_="next")
    if nut_next:
        url = base_url + nut_next.find("a")["href"]
    else:
        url = None

# 3. Ghi file CSV
with open(ten_file, mode="w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=["Quote", "Author", "Tags"])
    writer.writeheader()
    writer.writerows(danh_sach_quotes)

print(f"Xong! Đã lưu {len(danh_sach_quotes)} câu vào file {ten_file}")
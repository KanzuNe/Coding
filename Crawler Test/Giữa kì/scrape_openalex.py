import requests
import csv
import time
import json
import os

def scrape_openalex():
    base_url = "https://api.openalex.org/works"
    
    # Filter: Các bài báo thuộc các trường ở Việt Nam (institutions.country_code:VN)
    # Search: Liên quan đến Artificial Intelligence
    # Dùng mailto để được vào polite pool của OpenAlex (giúp request nhanh hơn và ít bị chặn)
    params = {
        'filter': 'institutions.country_code:VN,default.search:artificial intelligence',
        'per-page': 200,  # Max items per page
        'cursor': '*',     # Cursor-based pagination
        'mailto': 'student_project@example.com' 
    }
    
    csv_file = 'openalex_ai_vietnam.csv'
    fieldnames = ['Paper_ID', 'Title', 'Publication_Year', 'Citations', 'University_Name', 'Authors']
    
    print(f"Bắt đầu thu thập dữ liệu bài báo AI từ OpenAlex API...")
    
    total_papers = 0
    max_pages = 50 # Lấy tối đa 50 trang * 200 = 10.000 bài báo để file không quá khổng lồ nhưng đủ lớn
    
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        
        page = 1
        while params['cursor'] and page <= max_pages:
            print(f"Đang tải trang {page} (Cursor: {params['cursor'][:10]}...)...")
            
            try:
                response = requests.get(base_url, params=params, timeout=15)
                
                if response.status_code != 200:
                    print(f"Lỗi API (Status {response.status_code}): {response.text}")
                    break
                    
                data = response.json()
                results = data.get('results', [])
                
                if not results:
                    print("Đã hết dữ liệu.")
                    break
                
                rows_to_write = []
                for work in results:
                    paper_id = work.get('id', '').replace('https://openalex.org/', '')
                    title = work.get('title', '')
                    if not title: # Bỏ qua nếu không có tiêu đề
                        continue
                    
                    year = work.get('publication_year', '')
                    citations = work.get('cited_by_count', 0)
                    
                    # Tìm tên trường đại học ở Việt Nam
                    uni_names = []
                    authors = []
                    
                    for authorship in work.get('authorships', []):
                        # Tên tác giả
                        author_name = authorship.get('author', {}).get('display_name', '')
                        if author_name:
                            authors.append(author_name)
                            
                        # Tên trường
                        for inst in authorship.get('institutions', []):
                            if inst.get('country_code') == 'VN':
                                uni_name = inst.get('display_name', '')
                                if uni_name and uni_name not in uni_names:
                                    uni_names.append(uni_name)
                    
                    uni_str = " | ".join(uni_names)
                    authors_str = ", ".join(authors[:5]) # Chỉ lấy 5 tác giả đầu cho gọn
                    
                    rows_to_write.append({
                        'Paper_ID': paper_id,
                        'Title': title,
                        'Publication_Year': year,
                        'Citations': citations,
                        'University_Name': uni_str,
                        'Authors': authors_str
                    })
                
                writer.writerows(rows_to_write)
                total_papers += len(rows_to_write)
                print(f"--> Đã lưu {len(rows_to_write)} bài báo. Tổng cộng: {total_papers} bài.")
                
                # Cập nhật cursor cho trang tiếp theo
                next_cursor = data.get('meta', {}).get('next_cursor')
                params['cursor'] = next_cursor
                page += 1
                
                time.sleep(0.1) # Tạm nghỉ một chút để không vượt quá rate limit (10 req/s)
                
            except requests.exceptions.RequestException as e:
                print(f"Lỗi kết nối: {e}")
                time.sleep(2)
                
    print(f"\n✅ HOÀN THÀNH! Đã cào thành công {total_papers} bài báo AI từ OpenAlex vào file '{csv_file}'.")

if __name__ == "__main__":
    scrape_openalex()

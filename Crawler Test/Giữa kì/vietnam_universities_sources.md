# 🎓 Danh sách các nguồn dữ liệu Scrape (Cập nhật chiến lược mới)

Tài liệu này liệt kê chi tiết các nguồn dữ liệu đã được chuẩn hóa phục vụ cho Data Pipeline đánh giá năng lực nghiên cứu và xếp hạng ngành AI tại Việt Nam. Dữ liệu tập trung vào APIs và Ranking uy tín.

---

## 1. 📚 Nguồn 1: Data Học thuật & Lịch sử Nghiên cứu AI (OpenAlex API)

Nguồn chính: **OpenAlex API** (Miễn phí, không cần key, giới hạn 100,000 req/ngày. Là database mở lớn nhất thế giới về nghiên cứu).

- 🔗 **Endpoint bài báo (Works):** `https://api.openalex.org/works`
- **Cách lấy data cho các trường Việt Nam:** Lọc theo thông số `institutions.country_code:VN` và tìm kiếm keyword `Artificial Intelligence`.
- **Ví dụ Query API:** `https://api.openalex.org/works?filter=institutions.country_code:VN,concepts.id:https://openalex.org/C154945302,publication_year:2015-2024` 
- **Dữ liệu trích xuất:**
    - Tên trường Đại học chủ quản.
    - Năm xuất bản (Dùng vẽ Line chart).
    - Số lượt trích dẫn (Citations - Dùng vẽ Scatter/Heatmap).
    - Tiêu đề bài báo (Title - Dùng vẽ WordCloud).
- *🛠 **Công cụ dùng:*** `requests` (Python) gọi REST API, dùng json để bóc tách.

---

## 2. 💼 Nguồn 2: Data Thứ hạng Ngành AI tại Việt Nam (EduRank)

Thu thập thứ hạng thực tế của các trường Đại học tại Việt Nam dành riêng cho lĩnh vực Computer Science / Artificial Intelligence.

- **EduRank - Xếp hạng AI Việt Nam**
  - 🔗 **URL:** `https://edurank.org/cs/ai/vn/`
  - **Dữ liệu trích xuất:**
      - Tên 30+ trường Đại học có xếp hạng.
      - Rank Quốc gia (Vietnam Rank).
      - Rank Châu Á (Asia Rank).
      - Thành phố / Địa điểm (Dùng vẽ Bản đồ).
  - *🛠 **Công cụ dùng:*** `BeautifulSoup` + `requests`. Trang web dạng Table HTML rất dễ cào.

---

## 3. 🎯 Danh sách 30 Trường Đại học Mục tiêu
(Danh sách này dùng làm Base Dataset để đối chiếu/merge dữ liệu từ OpenAlex và EduRank. Các Tên tiếng Anh/Alias sẽ giúp tăng độ chính xác khi match data giữa 2 nguồn)

1. Đại học Bách khoa Hà Nội (HUST) - **Alias:** Hanoi University of Science and Technology
2. Đại học Công nghệ, ĐHQGHN (UET) - **Alias:** VNU University of Engineering and Technology / Vietnam National University, Hanoi
3. Đại học Khoa học Tự nhiên, ĐHQGHN (HUS) - **Alias:** VNU University of Science / Vietnam National University, Hanoi
4. Đại học Bách khoa, ĐHQG-HCM (HCMUT) - **Alias:** Ho Chi Minh City University of Technology
5. Đại học Công nghệ Thông tin, ĐHQG-HCM (UIT) - **Alias:** University of Information Technology - VNUHCM
6. Đại học Khoa học Tự nhiên, ĐHQG-HCM (HCMUS) - **Alias:** University of Science, VNU-HCM
7. Đại học Bách khoa, ĐH Đà Nẵng (DUT) - **Alias:** Danang University of Science and Technology
8. Học viện Công nghệ Bưu chính Viễn thông (PTIT) - **Alias:** Posts and Telecommunications Institute of Technology
9. Học viện Kỹ thuật Quân sự (MTA) - **Alias:** Military Technical Academy / Le Quy Don Technical University
10. Học viện Kỹ thuật Mật mã (KMA) - **Alias:** Academy of Cryptography Techniques
11. Đại học Sư phạm Kỹ thuật TP.HCM (HCMUTE) - **Alias:** Ho Chi Minh City University of Technology and Education
12. Đại học Công nghiệp Hà Nội (HaUI) - **Alias:** Hanoi University of Industry
13. Đại học Công nghiệp TP.HCM (IUH) - **Alias:** Industrial University of Ho Chi Minh City
14. Đại học Giao thông Vận tải (UTC) - **Alias:** University of Transport and Communications
15. Đại học Thủy lợi (TLU) - **Alias:** Thuyloi University / Water Resources University
16. Đại học Xây dựng Hà Nội (HUCE) - **Alias:** Hanoi University of Civil Engineering
17. Đại học Mỏ - Địa chất (HUMG) - **Alias:** Hanoi University of Mining and Geology
18. Đại học Mở Hà Nội (HOU) - **Alias:** Hanoi Open University
19. Đại học Khoa học và Công nghệ Hà Nội (USTH - ĐH Việt Pháp) - **Alias:** University of Science and Technology of Hanoi / Vietnam France University
20. Đại học Cần Thơ (CTU) - **Alias:** Can Tho University
21. Đại học Khoa học, ĐH Huế (HUSC) - **Alias:** University of Science, Hue University
22. Đại học Quốc tế, ĐHQG-HCM (HCMIU) - **Alias:** International University, VNU-HCM
23. Đại học FPT (FPTU) - **Alias:** FPT University
24. Đại học Tôn Đức Thắng (TDTU) - **Alias:** Ton Duc Thang University
25. Đại học RMIT Việt Nam (RMIT) - **Alias:** RMIT University Vietnam
26. Đại học Duy Tân (DTU) - **Alias:** Duy Tan University
27. Đại học Phenikaa (PU) - **Alias:** Phenikaa University
28. Đại học Văn Lang (VLU) - **Alias:** Van Lang University
29. Đại học Công nghệ TP.HCM (HUTECH) - **Alias:** Ho Chi Minh City University of Technology (HUTECH)
30. Đại học Hoa Sen (HSU) - **Alias:** Hoa Sen University

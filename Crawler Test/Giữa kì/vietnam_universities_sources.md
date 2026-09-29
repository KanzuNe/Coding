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
(Danh sách này dùng làm Base Dataset để đối chiếu/merge dữ liệu từ OpenAlex và EduRank)

1. Đại học Bách khoa Hà Nội (HUST)
2. Đại học Công nghệ, ĐHQGHN (UET)
3. Đại học Khoa học Tự nhiên, ĐHQGHN (HUS)
4. Đại học Bách khoa, ĐHQG-HCM (HCMUT)
5. Đại học Công nghệ Thông tin, ĐHQG-HCM (UIT)
6. Đại học Khoa học Tự nhiên, ĐHQG-HCM (HCMUS)
7. Đại học Bách khoa, ĐH Đà Nẵng (DUT)
8. Học viện Công nghệ Bưu chính Viễn thông (PTIT)
9. Học viện Kỹ thuật Quân sự (MTA)
10. Học viện Kỹ thuật Mật mã (KMA)
11. Đại học Sư phạm Kỹ thuật TP.HCM (HCMUTE)
12. Đại học Công nghiệp Hà Nội (HaUI)
13. Đại học Công nghiệp TP.HCM (IUH)
14. Đại học Giao thông Vận tải (UTC)
15. Đại học Thủy lợi (TLU)
16. Đại học Xây dựng Hà Nội (HUCE)
17. Đại học Mỏ - Địa chất (HUMG)
18. Đại học Mở Hà Nội (HOU)
19. Đại học Khoa học và Công nghệ Hà Nội (USTH - ĐH Việt Pháp)
20. Đại học Cần Thơ (CTU)
21. Đại học Khoa học, ĐH Huế (HUSC)
22. Đại học Quốc tế, ĐHQG-HCM (HCMIU)
23. Đại học FPT (FPTU)
24. Đại học Tôn Đức Thắng (TDTU)
25. Đại học RMIT Việt Nam (RMIT)
26. Đại học Duy Tân (DTU)
27. Đại học Phenikaa (PU)
28. Đại học Văn Lang (VLU)
29. Đại học Công nghệ TP.HCM (HUTECH)
30. Đại học Hoa Sen (HSU)

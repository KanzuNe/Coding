# 🎓 Danh sách các nguồn dữ liệu Scrape cho 30 trường Đại học tại Việt Nam

Tài liệu này liệt kê chi tiết các nguồn dữ liệu cụ thể phục vụ cho Data Pipeline đánh giá năng lực đào tạo, nghiên cứu và việc làm ngành AI tại Việt Nam.

---

## 1. 📥 Nguồn 1: Data Đào tạo & Chi phí (Web Scraping từ Website các trường)

Dưới đây là danh sách 30 trường Đại học tiêu biểu có đào tạo ngành Công nghệ thông tin / Trí tuệ nhân tạo (AI) / Khoa học dữ liệu tại Việt Nam. Đây sẽ là mục tiêu để cào dữ liệu học phí, thời gian đào tạo và mô tả chương trình.

### Khối Đại học Quốc gia & Công lập hàng đầu (Top-tier)
1. **Đại học Bách khoa Hà Nội (HUST)** - [hust.edu.vn](https://hust.edu.vn) | [ts.hust.edu.vn](https://ts.hust.edu.vn)
2. **Đại học Công nghệ, ĐHQGHN (UET)** - [uet.vnu.edu.vn](https://uet.vnu.edu.vn)
3. **Đại học Khoa học Tự nhiên, ĐHQGHN (HUS)** - [hus.vnu.edu.vn](https://hus.vnu.edu.vn)
4. **Đại học Bách khoa, ĐHQG-HCM (HCMUT)** - [hcmut.edu.vn](https://hcmut.edu.vn)
5. **Đại học Công nghệ Thông tin, ĐHQG-HCM (UIT)** - [uit.edu.vn](https://uit.edu.vn)
6. **Đại học Khoa học Tự nhiên, ĐHQG-HCM (HCMUS)** - [hcmus.edu.vn](https://hcmus.edu.vn)
7. **Đại học Bách khoa, ĐH Đà Nẵng (DUT)** - [dut.udn.vn](https://dut.udn.vn)

### Khối Công lập Kỹ thuật - Công nghệ
8. **Học viện Công nghệ Bưu chính Viễn thông (PTIT)** - [ptit.edu.vn](https://ptit.edu.vn)
9. **Học viện Kỹ thuật Quân sự (MTA)** - [mta.edu.vn](https://mta.edu.vn)
10. **Học viện Kỹ thuật Mật mã (KMA)** - [actvn.edu.vn](https://actvn.edu.vn)
11. **Đại học Sư phạm Kỹ thuật TP.HCM (HCMUTE)** - [hcmute.edu.vn](https://hcmute.edu.vn)
12. **Đại học Công nghiệp Hà Nội (HaUI)** - [haui.edu.vn](https://haui.edu.vn)
13. **Đại học Công nghiệp TP.HCM (IUH)** - [iuh.edu.vn](https://iuh.edu.vn)
14. **Đại học Giao thông Vận tải (UTC)** - [utc.edu.vn](https://utc.edu.vn)
15. **Đại học Thủy lợi (TLU)** - [tlu.edu.vn](https://tlu.edu.vn)
16. **Đại học Xây dựng Hà Nội (HUCE)** - [huce.edu.vn](https://huce.edu.vn)
17. **Đại học Mỏ - Địa chất (HUMG)** - [humg.edu.vn](https://humg.edu.vn)
18. **Đại học Mở Hà Nội (HOU)** - [hou.edu.vn](https://hou.edu.vn)
19. **Đại học Khoa học và Công nghệ Hà Nội (USTH - ĐH Việt Pháp)** - [usth.edu.vn](https://usth.edu.vn)

### Khối Đại học Vùng / Khu vực
20. **Đại học Cần Thơ (CTU)** - [ctu.edu.vn](https://ctu.edu.vn)
21. **Đại học Khoa học, ĐH Huế (HUSC)** - [husc.hueuni.edu.vn](https://husc.hueuni.edu.vn)
22. **Đại học Quốc tế, ĐHQG-HCM (HCMIU)** - [hcmiu.edu.vn](https://hcmiu.edu.vn)

### Khối Dân lập / Tư thục / Quốc tế
23. **Đại học FPT (FPTU)** - [fpt.edu.vn](https://fpt.edu.vn)
24. **Đại học Tôn Đức Thắng (TDTU)** - [tdtu.edu.vn](https://tdtu.edu.vn)
25. **Đại học RMIT Việt Nam (RMIT)** - [rmit.edu.vn](https://rmit.edu.vn)
26. **Đại học Duy Tân (DTU)** - [duytan.edu.vn](https://duytan.edu.vn)
27. **Đại học Phenikaa (PU)** - [phenikaa-uni.edu.vn](https://phenikaa-uni.edu.vn)
28. **Đại học Văn Lang (VLU)** - [vlu.edu.vn](https://vlu.edu.vn)
29. **Đại học Công nghệ TP.HCM (HUTECH)** - [hutech.edu.vn](https://hutech.edu.vn)
30. **Đại học Hoa Sen (HSU)** - [hoasen.edu.vn](https://hoasen.edu.vn)

*🛠 **Cách scrape gợi ý:*** 
- Sử dụng `BeautifulSoup` và `requests` kết hợp với Google Search (Search "Tên trường + học phí / chương trình đào tạo AI") để lấy link đích.
- Một số trang web của trường sử dụng SPA (Single Page Application) có thể yêu cầu dùng `Playwright`.

---

## 2. 📚 Nguồn 2: Data Học thuật & Lịch sử (Số bài báo AI)

Nguồn chính: **OpenAlex API** (Miễn phí, không cần key, giới hạn 100,000 req/ngày).
- 🔗 **Endpoint:** `https://api.openalex.org/works`
- **Cách lấy data cho các trường Việt Nam:** Lọc theo thông số `institutions.country_code:VN` và tìm kiếm keyword `Artificial Intelligence` hoặc lọc theo `concepts`.
- **Ví dụ Query API:** `https://api.openalex.org/works?filter=institutions.country_code:VN,concepts.id:https://openalex.org/C154945302,publication_year:2014-2024&group_by=institutions.id` 
- *🛠 **Công cụ gợi ý:*** `requests` (Python) gọi REST API.

---

## 3. 💼 Nguồn 3: Data Cơ hội Việc làm & Ranking tại Việt Nam

Thu thập điểm danh tiếng nhà tuyển dụng, sức hút công nghiệp và xếp hạng của các trường VN.

- **QS World University Rankings (Asia / Vietnam)**
  - 🔗 **URL:** `https://www.topuniversities.com/asia-university-rankings?country=VN`
  - **Data lấy:** Employer Reputation, Academic Reputation, v.v.
  - *🛠 **Công cụ gợi ý:*** QS chặn bot khá gắt, nên dùng `Playwright` hoặc tìm file JSON API ẩn từ network tab.

- **THE (Times Higher Education) - Vietnam**
  - 🔗 **URL:** `https://www.timeshighereducation.com/world-university-rankings/2024/world-ranking#!/length/25/locations/VNM/sort_by/rank/sort_order/asc/cols/stats`
  - **Data lấy:** Industry Income (Thu nhập từ liên kết doanh nghiệp).
  - *🛠 **Công cụ gợi ý:*** Lấy API ẩn trả về JSON qua tab Network.

- **EduRank (Dữ liệu tổng hợp)**
  - 🔗 **URL:** `https://edurank.org/cs/ai/vn/`
  - **Data lấy:** Ranking ngành AI cụ thể tại VN, có thể cào luôn cả thông tin học phí sơ bộ.
  - *🛠 **Công cụ gợi ý:*** `BeautifulSoup` + `requests`.

- **Webometrics (Xếp hạng mức độ ảnh hưởng)**
  - 🔗 **URL:** `https://www.webometrics.info/en/asia/vietnam`
  - **Data lấy:** Tầm ảnh hưởng trên web, độ mở học thuật (Openness Rank).
  - *🛠 **Công cụ gợi ý:*** `BeautifulSoup` (Rất dễ scrape, web thuần HTML).

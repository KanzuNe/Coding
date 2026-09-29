# 📊 Data Pipeline & Kế hoạch Triển khai (Bài tập giữa kỳ)

**Chủ đề:** Đánh giá năng lực đào tạo, nghiên cứu và cơ hội việc làm ngành AI tại các trường Đại học (Nhật Bản vs Việt Nam).

## 1. 📥 Data Collection (Thu thập dữ liệu)
Thu thập từ 3 nguồn để tạo thành một bảng Master Dataset toàn diện:

*   **Nguồn 1: Data Đào tạo & Chi phí (Web Scraping)**
    *   **Nguồn:** Các trang Aggregator (Ví dụ: bachelorsportal.com, mastersportal.com, hoặc jasso.go.jp).
    *   **Dữ liệu cần lấy:** `Tên trường`, `Quốc gia` (VN/JP), `Thành phố`, `Học phí/năm`, `Thời gian đào tạo (Năm)`, `Mô tả chương trình`.
    *   **Công cụ:** `requests`, `BeautifulSoup`.
*   **Nguồn 2: Data Học thuật & Lịch sử (Dùng API)**
    *   **Nguồn:** OpenAlex API (Cơ sở dữ liệu nghiên cứu mở).
    *   **Dữ liệu cần lấy:** `Số lượng bài báo về AI` của từng trường, phân bổ theo từng `Năm` (từ 2014 - 2024).
    *   **Công cụ:** `requests` (gọi REST API lấy JSON).
*   **Nguồn 3: Data Cơ hội Việc làm (Web Scraping/Proxy Data)**
    *   **Nguồn:** QS World University Rankings hoặc THE Rankings.
    *   **Dữ liệu cần lấy:** Điểm số `Employer Reputation` (Danh tiếng nhà tuyển dụng) hoặc `Industry Income` (Điểm thu hút vốn công nghiệp).
    *   **Công cụ:** `requests`, `BeautifulSoup`.

## 2. ⚙️ Data Preprocessing & Merging (Tiền xử lý)
*   **Làm sạch (Cleaning):** 
    *   Chuẩn hóa tên trường (bước cốt lõi vì các nguồn có thể viết tên khác nhau, VD: "HUST" vs "Hanoi University of Science and Technology"). *Gợi ý: Dùng thư viện `fuzzywuzzy` để match tên trường.*
    *   Đổi `Học phí` về cùng một đơn vị (Ví dụ: USD).
*   **Xử lý Missing Data:** 
    *   Dùng `fillna()` bằng giá trị trung bình/trung vị (mean/median) cho các trường bị thiếu điểm Xếp hạng hoặc Học phí.
*   **Ghép bảng (Merge):** Dùng `pd.merge()` ghép 3 bảng dữ liệu lại với Key là `Tên trường`.
*   **Feature Engineering (Tạo cột mới):**
    *   `Tổng chi phí` = `Học phí/năm` * `Thời gian đào tạo`.
    *   Phân loại trường bằng `pd.cut()`: `Nhóm học phí cao`, `Nhóm trung bình`, `Nhóm thấp`.

## 3. 📈 Data Visualization (Trực quan hóa - Đáp ứng đủ 7 yêu cầu)

1.  **Histogram / Boxplot:** Vẽ phân phối của `Học phí` hoặc `Điểm Việc làm (Employer Score)` giữa VN và Nhật. Xem nước nào có mức dao động lớn hơn.
2.  **Line / Area (Time Series):** Xu hướng `Số lượng bài nghiên cứu AI` tăng trưởng qua các năm (2014-2024), chia thành 2 line (Nhật và VN).
3.  **Scatter + Hồi quy:** Trục X là `Số lượng nghiên cứu`, Trục Y là `Điểm Việc làm`. (Kiểm chứng giả thuyết: Trường nghiên cứu nhiều thì doanh nghiệp có thích/ưu tiên tuyển dụng hơn không?).
4.  **Heatmap (Tương quan):** Ma trận tương quan giữa các biến số số học: `Học phí`, `Số bài Nghiên cứu`, `Điểm việc làm`, `Thời gian học`.
5.  **Bản đồ (Folium) / Treemap:** Dùng cột `Thành phố` để chấm điểm tọa độ các trường lên bản đồ Map, qua đó thấy được "AI Hub" (điểm nóng đào tạo) nằm ở đâu.
6.  **WordCloud:** Gom cột `Mô tả chương trình`, tạo đám mây từ vựng so sánh keyword đào tạo của VN (ví dụ: Software, System, Data) vs Nhật Bản (ví dụ: Robotics, Hardware, Embedded).
7.  **Interactive Charts (Plotly/Altair):** Áp dụng Plotly cho Line chart, Scatter chart và Bản đồ để tương tác (hover chuột xem tên trường chi tiết).

## 4. 📝 Storytelling & Báo cáo
*   **Thông điệp chính (Key Insight):** Bức tranh toàn cảnh về ROI (Return on Investment) khi học AI. 
    *   Nhật Bản có thể có học phí cao, nhưng đầu tư mạnh vào nghiên cứu hàn lâm và có liên kết công nghiệp chặt chẽ (đầu ra việc làm uy tín).
    *   Việt Nam tập trung đào tạo linh hoạt, thực chiến, số lượng nghiên cứu đang có đà tăng tốc rất nhanh.
    *   Học phí cao chưa chắc đã đi kèm với điểm việc làm tốt, mà yếu tố cốt lõi có thể nằm ở hệ sinh thái hợp tác doanh nghiệp của trường đó.

## 5. 💻 Frontend Dashboard (Giao diện hiển thị)
*   **Phong cách thiết kế (UI/UX):** Giao diện Dark mode, mượt mà và sắc nét mang hơi hướng của các hệ thống quản trị server/homelab (như Portainer, CasaOS, Proxmox) và Cloudflare.
*   **Bố cục (Layout):** Sử dụng các Grid/Card (Bảng điều khiển) vuông vức, hiển thị các chỉ số (Metrics) nổi bật và đóng gói các biểu đồ một cách gọn gàng, tạo cảm giác "Premium" và "Tech-savvy".
*   **Tích hợp Data:** Dữ liệu sau khi xử lý ở Jupyter Notebook sẽ được xuất ra và kết nối thông qua API (có thể là một web server nhỏ bằng Flask/FastAPI) để đẩy lên Frontend.
*   **Lộ trình thực hiện:** Phần code giao diện và liên kết API sẽ được thực hiện ở phase sau (sau khi đã hoàn thành và chốt phần Data Pipeline).

# 📊 Data Pipeline & Kế hoạch Triển khai (Bài tập giữa kỳ)

**Chủ đề:** Đánh giá năng lực nghiên cứu, chất lượng đào tạo và thứ hạng ngành AI tại các trường Đại học ở Việt Nam.
*(Lưu ý: Đánh giá thông qua dữ liệu nghiên cứu khoa học và bảng xếp hạng quốc tế do dữ liệu việc làm thực tế trên website các trường bị thiếu và không đồng nhất).*

## 1. 📥 Data Collection (Thu thập dữ liệu)
Thu thập từ 2 nguồn chính với dữ liệu chất lượng cao và có cấu trúc:

*   **Nguồn 1: Data Thành tích Nghiên cứu AI (Dùng API)**
    *   **Nguồn:** OpenAlex API (Cơ sở dữ liệu nghiên cứu khoa học mở lớn nhất).
    *   **Dữ liệu cần lấy:** `Tên trường`, `Số lượng bài báo về AI` (từ 2015 - 2024), `Tổng số lượt trích dẫn (Citations)`, `Tiêu đề bài báo (Title)`.
    *   **Công cụ:** `requests` (gọi REST API lấy JSON).
*   **Nguồn 2: Data Thứ hạng & Xếp hạng ngành AI (Web Scraping)**
    *   **Nguồn:** EduRank (Chuyên trang xếp hạng đại học, có rank riêng cho ngành AI tại VN).
    *   **Dữ liệu cần lấy:** `Tên trường`, `Hạng ngành AI (VN)`, `Hạng ngành AI (Châu Á)`, `Thành phố`.
    *   **Công cụ:** `requests`, `BeautifulSoup`.

## 2. ⚙️ Data Preprocessing & Merging (Tiền xử lý)
*   **Làm sạch (Cleaning):** 
    *   Chuẩn hóa tên trường (bước cốt lõi vì OpenAlex dùng tên tiếng Anh/quốc tế, còn EduRank có thể dùng tên tiếng Việt/Anh khác biệt). *Gợi ý: Dùng thư viện `fuzzywuzzy` để match tên trường.*
*   **Xử lý Missing Data:** 
    *   Loại bỏ các trường không có dữ liệu xếp hạng AI hoặc điền giá trị trung bình/ngoại lệ nếu cần thiết.
*   **Ghép bảng (Merge):** Dùng `pd.merge()` ghép 2 bảng dữ liệu lại với Key là `Tên trường đã chuẩn hóa`.
*   **Feature Engineering (Tạo cột mới):**
    *   `Tỷ lệ Trích dẫn/Bài báo` = `Citations` / `Số lượng bài báo`.
    *   Phân loại trường: `Top 5`, `Top 10`, `Top 30`.

## 3. 📈 Data Visualization (Trực quan hóa - Đáp ứng đủ 7 yêu cầu)

1.  **Histogram / Boxplot:** Vẽ phân bố số lượng `Trích dẫn (Citations)` của các trường ĐH tại Việt Nam để xem mức độ chênh lệch nghiên cứu giữa các nhóm trường.
2.  **Line / Area (Time Series):** Xu hướng `Số lượng bài báo AI` được công bố qua các năm (2015-2024), so sánh sự tăng tốc của Top 5 trường đại học dẫn đầu.
3.  **Scatter + Hồi quy:** Trục X là `Số bài báo (Nghiên cứu)`, Trục Y là `Thứ hạng Châu Á (EduRank)`. (Kiểm chứng giả thuyết: Trường nào có nhiều nghiên cứu AI thì thứ hạng quốc tế càng cao).
4.  **Heatmap (Tương quan):** Ma trận tương quan giữa: `Số bài báo`, `Số trích dẫn`, `Thứ hạng Quốc gia`, `Thứ hạng Châu Á`.
5.  **Bản đồ (Folium) / Treemap:** Dùng cột `Thành phố` để vẽ Bubble Map (bản đồ bong bóng) tại VN. Vòng tròn to/nhỏ thể hiện "sức mạnh nghiên cứu AI" của từng khu vực.
6.  **WordCloud:** Gom cột `Tiêu đề bài báo` (Title/Abstract) từ OpenAlex, tạo đám mây từ vựng để phân tích xem giới hàn lâm AI tại VN đang tập trung nghiên cứu keyword nào (ví dụ: Deep Learning, Neural Network, Image Processing...).
7.  **Interactive Charts (Plotly/Altair):** Áp dụng Plotly cho biểu đồ Scatter. Khi hover chuột sẽ hiện popup thông tin chi tiết (VD: "Đại học Bách khoa HN - 500 bài báo - Hạng 1 VN").

## 4. 📝 Storytelling & Báo cáo
*   **Thông điệp chính (Key Insight):** Bức tranh toàn cảnh về sức mạnh học thuật và năng lực đào tạo ngành AI tại Việt Nam.
    *   Các trường công nghệ lâu đời có đang thống trị mảng nghiên cứu AI, hay có sự trỗi dậy của các trường tư thục?
    *   Chất lượng nghiên cứu (Tỷ lệ trích dẫn) có tương xứng với số lượng bài báo?
    *   Các thành phố "đầu tàu" (Hà Nội, TP.HCM, Đà Nẵng) đóng góp tỷ trọng bao nhiêu vào tổng lực lượng nghiên cứu AI của Việt Nam?

## 5. 💻 Frontend Dashboard (Giao diện hiển thị)
*   **Phong cách thiết kế (UI/UX):** Phong cách chuyên nghiệp, tối giản. Tông màu chủ đạo: Trắng và Xanh trời nhẹ (Light Blue), tạo cảm giác sạch sẽ, dễ nhìn.
*   **Bố cục (Layout):**
    *   Sử dụng Sidebar kết hợp Tabs để phân chia các nhóm biểu đồ có liên quan (VD: Tổng quan, Phân bố khu vực, Tương quan học thuật).
    *   Bố cục trình bày theo hướng Storytelling (kể chuyện dữ liệu): mỗi biểu đồ sẽ đi kèm phần text nhận xét/so sánh bên cạnh giống như trang giới thiệu sản phẩm.
*   **Tích hợp Data:** Xuất thẳng toàn bộ kết quả phân tích và biểu đồ Plotly thành một file `index.html` tĩnh độc lập (Standalone). Đảm bảo giáo viên chỉ cần click đúp mở file `index.html` trên trình duyệt bất kỳ là mọi biểu đồ tự động hiển thị đầy đủ, không phụ thuộc vào Python hay môi trường cài đặt.

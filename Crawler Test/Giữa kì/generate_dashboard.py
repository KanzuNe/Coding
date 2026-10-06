import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import io
import base64

print("Generating static HTML Dashboard...")

# Load data
df_merged = pd.read_csv('cleaned_merged_data.csv')
df_oa = pd.read_csv('cleaned_openalex_ai_vietnam.csv')

def style_fig(fig):
    fig.update_layout(
        template='plotly_white',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20),
        font=dict(family="Inter, sans-serif", color="#334155")
    )
    return fig

labels_dict = {
    'AI_Citations': 'Trích dẫn',
    'AI_Publications': 'Số bài báo',
    'University_Name': 'Trường Đại học',
    'City': 'Thành phố',
    'Publication_Year': 'Năm xuất bản',
    'Paper_ID': 'Số bài báo',
    'Vietnam_Rank': 'Hạng VN',
    'Acceptance_Rate': 'Tỉ lệ đỗ',
    'lat': 'Vĩ độ',
    'lon': 'Kinh độ'
}

# 1. Boxplot
fig1 = px.box(df_merged, y='AI_Citations', hover_name='University_Name', log_y=True, title='Phân bố lượng trích dẫn AI (Log Scale)', labels=labels_dict)
fig1 = style_fig(fig1)
html1 = fig1.to_html(full_html=False, include_plotlyjs=False)

# 2. Line Chart
df_year = df_oa.groupby('Publication_Year')['Paper_ID'].count().reset_index()
df_year = df_year[df_year['Publication_Year'] >= 2010]
fig2 = px.line(df_year, x='Publication_Year', y='Paper_ID', title='Số lượng bài báo AI qua các năm (từ 2010)', labels=labels_dict)
fig2 = style_fig(fig2)
fig2.update_traces(line_color='#0ea5e9', line_width=3)
html2 = fig2.to_html(full_html=False, include_plotlyjs=False)

# 3. Scatter
# Yêu cầu bổ sung hồi quy (trendline) - thêm trendline='ols'
df_scatter = df_merged.dropna(subset=['AI_Publications', 'AI_Citations'])
fig3 = px.scatter(df_scatter, x='AI_Publications', y='AI_Citations', title='Tương quan Số bài báo & Trích dẫn', hover_data=['University_Name'], trendline='ols', trendline_color_override='red', labels=labels_dict)
fig3 = style_fig(fig3)
html3 = fig3.to_html(full_html=False, include_plotlyjs=False)

# 4. Treemap
df_clean = df_merged.dropna(subset=['City', 'University_Name'])
fig4 = px.treemap(df_clean, path=['City', 'University_Name'], values='AI_Publications', title='Phân bố bài báo theo Thành phố', labels=labels_dict)
fig4 = style_fig(fig4)
html4 = fig4.to_html(full_html=False, include_plotlyjs=False)

# 4b. Map
city_coords = {
    'Hanoi': (21.0285, 105.8542),
    'Ho Chi Minh': (10.8231, 106.6297),
    'Da Nang': (16.0544, 108.2022),
    'Can Tho': (10.0452, 105.7469),
    'Vinh': (18.6733, 105.6813),
    'Haiphong': (20.8449, 106.6881),
    'Nha Trang': (12.2388, 109.1967)
}
df_map = df_merged.dropna(subset=['City']).copy()
df_map['lat'] = df_map['City'].map(lambda x: city_coords.get(x, (0,0))[0])
df_map['lon'] = df_map['City'].map(lambda x: city_coords.get(x, (0,0))[1])
fig_map = px.scatter_map(
    df_map, lat="lat", lon="lon", 
    hover_name="University_Name",
    hover_data=["City", "AI_Publications"],
    size="AI_Publications",
    color="AI_Publications",
    color_continuous_scale="Blues",
    zoom=4.5,
    center={"lat": 16.0, "lon": 106.0}, 
    title="Phân bố các trường Đại học trên bản đồ Việt Nam",
    labels=labels_dict
)
fig_map.update_layout(map_style="open-street-map", margin={"r":20,"t":40,"l":20,"b":20}, font=dict(family="Inter, sans-serif", color="#334155"))
html_map = fig_map.to_html(full_html=False, include_plotlyjs=False)

# 5. Heatmap
df_numeric = df_merged[['Vietnam_Rank', 'Acceptance_Rate', 'AI_Publications', 'AI_Citations']]
df_numeric = df_numeric.rename(columns=labels_dict)
fig5 = px.imshow(df_numeric.corr(), text_auto=True, title='Heatmap ma trận tương quan', color_continuous_scale='Blues')
fig5 = style_fig(fig5)
html5 = fig5.to_html(full_html=False, include_plotlyjs=False)

# 6. WordCloud
text = ' '.join(str(title) for title in df_oa['Title'].dropna())
wc = WordCloud(width=800, height=400, background_color='white', colormap='Blues').generate(text)
img = io.BytesIO()
wc.to_image().save(img, format='PNG')
img_b64 = base64.b64encode(img.getvalue()).decode()
wc_html = f'<img src="data:image/png;base64,{img_b64}" alt="WordCloud" class="wordcloud-img"/>'

total_pubs = int(df_merged['AI_Publications'].sum())
total_cites = int(df_merged['AI_Citations'].sum())

# HTML Template with Sidebar, Tabs and Light Blue/White Theme
html_template = f"""
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Báo cáo Năng lực Nghiên cứu AI tại Việt Nam</title>
    <!-- Load Plotly once globally -->
    <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary-blue: #0ea5e9;
            --bg-color: #f8fafc;
            --sidebar-bg: #ffffff;
            --text-main: #334155;
            --text-muted: #64748b;
            --border-color: #e2e8f0;
        }}
        body {{ 
            margin: 0; font-family: 'Inter', sans-serif; background-color: var(--bg-color); color: var(--text-main); 
            display: flex; height: 100vh; overflow: hidden; 
        }}
        .sidebar {{ 
            width: 280px; background: var(--sidebar-bg); border-right: 1px solid var(--border-color); 
            padding: 30px 0; display: flex; flex-direction: column; flex-shrink: 0;
        }}
        .sidebar-title {{ 
            font-size: 1.4rem; font-weight: 700; color: var(--primary-blue); padding: 0 20px; margin-bottom: 40px; 
            text-align: center;
        }}
        .tab-btn {{ 
            padding: 15px 25px; border: none; background: none; text-align: left; font-size: 1.05rem; 
            color: var(--text-muted); cursor: pointer; border-left: 4px solid transparent; 
            transition: all 0.2s; font-weight: 600;
        }}
        .tab-btn:hover {{ background: #f1f5f9; color: var(--text-main); }}
        .tab-btn.active {{ color: var(--primary-blue); border-left-color: var(--primary-blue); background: #f0f9ff; }}
        
        .main-content {{ flex: 1; overflow-y: auto; padding: 40px 60px; scroll-behavior: smooth; }}
        .tab-content {{ display: none; animation: fadeIn 0.4s ease; }}
        .tab-content.active {{ display: block; }}
        @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        
        .header-title {{ margin-top: 0; font-size: 2.2rem; color: var(--text-main); margin-bottom: 30px; }}
        
        .story-section {{ 
            display: flex; gap: 40px; margin-bottom: 50px; background: #fff; padding: 30px; 
            border-radius: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -1px rgba(0,0,0,0.03); 
            align-items: center; border: 1px solid var(--border-color);
        }}
        .story-section.reverse {{ flex-direction: row-reverse; }}
        .story-text {{ flex: 1; }}
        .story-chart {{ flex: 2; min-width: 0; }} /* min-width 0 allows plotly to resize down */
        
        .story-text h2 {{ font-size: 1.6rem; color: var(--text-main); margin-top: 0; margin-bottom: 15px; }}
        .story-text p {{ font-size: 1.05rem; line-height: 1.7; color: var(--text-muted); }}
        
        .kpi-row {{ display: flex; gap: 30px; margin-bottom: 40px; }}
        .kpi-card {{ 
            flex: 1; background: #fff; padding: 30px; border-radius: 16px; 
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); text-align: center; 
            border-bottom: 4px solid var(--primary-blue); border: 1px solid var(--border-color);
        }}
        .kpi-val {{ font-size: 3rem; font-weight: 700; color: var(--primary-blue); }}
        .kpi-label {{ font-size: 0.95rem; text-transform: uppercase; color: var(--text-muted); letter-spacing: 1px; margin-top: 10px; font-weight: 600;}}
        
        .wordcloud-img {{ max-width: 100%; height: auto; border-radius: 12px; }}
    </style>
</head>
<body>
    <div class="sidebar">
        <div class="sidebar-title">VNAI Research Insight</div>
        <button class="tab-btn active" onclick="openTab(event, 'tab1')">1. Tổng quan & Xu hướng</button>
        <button class="tab-btn" onclick="openTab(event, 'tab2')">2. Phân bố Khu vực</button>
        <button class="tab-btn" onclick="openTab(event, 'tab3')">3. Chất lượng & Tương quan</button>
    </div>
    
    <div class="main-content">
        <!-- Tab 1 -->
        <div id="tab1" class="tab-content active">
            <h1 class="header-title">Bức tranh toàn cảnh Nghiên cứu AI</h1>
            <div class="kpi-row">
                <div class="kpi-card">
                    <div class="kpi-val">{total_pubs:,}</div>
                    <div class="kpi-label">Tổng bài báo AI</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-val">{total_cites:,}</div>
                    <div class="kpi-label">Tổng trích dẫn</div>
                </div>
            </div>
            
            <div class="story-section">
                <div class="story-text">
                    <h2>Sự bùng nổ nghiên cứu AI</h2>
                    <p>Trong thập kỷ qua, số lượng công bố khoa học về Trí tuệ Nhân tạo tại Việt Nam đã có sự tăng trưởng đáng kể. Đặc biệt từ sau năm 2018, số lượng bài báo tăng vọt, cho thấy sự hòa nhập của các trường đại học vào làn sóng công nghệ 4.0 trên toàn cầu.</p>
                </div>
                <div class="story-chart">{html2}</div>
            </div>
            
            <div class="story-section reverse">
                <div class="story-text">
                    <h2>Từ khóa nghiên cứu cốt lõi</h2>
                    <p>Đám mây từ vựng (WordCloud) được trích xuất từ tiêu đề của hàng ngàn bài báo cho thấy các học giả Việt Nam đang tập trung vào các nhánh chính yếu của AI như Deep Learning, Machine Learning, Neural Networks và các ứng dụng trong Computer Vision hay Medical Imaging.</p>
                </div>
                <div class="story-chart" style="text-align: center;">{wc_html}</div>
            </div>
        </div>
        
        <!-- Tab 2 -->
        <div id="tab2" class="tab-content">
            <h1 class="header-title">Phân bố Năng lực theo Khu vực</h1>
            
            <div class="story-section">
                <div class="story-text">
                    <h2>Bản đồ phân bố AI</h2>
                    <p>Bản đồ dưới đây thể hiện quy mô nghiên cứu AI dựa trên vị trí địa lý. Kích thước vòng tròn tỷ lệ thuận với số lượng bài báo AI. Có thể thấy rõ sự tập trung đông đảo ở các thành phố lớn.</p>
                </div>
                <div class="story-chart">{html_map}</div>
            </div>
            
            <div class="story-section reverse">
                <div class="story-text">
                    <h2>Đầu tàu công nghệ: Hà Nội & TP.HCM</h2>
                    <p>Biểu đồ Treemap minh họa rõ nét sự phân bổ học thuật tại Việt Nam. Hai trung tâm kinh tế lớn nhất cả nước là Hà Nội và TP.HCM đang chiếm lĩnh diện tích lớn nhất, đóng vai trò dẫn dắt lực lượng nghiên cứu AI của toàn quốc. Các trường như Đại học Bách Khoa, Đại học Quốc Gia đang duy trì vị thế đứng đầu vững chắc.</p>
                </div>
                <div class="story-chart">{html4}</div>
            </div>
        </div>
        
        <!-- Tab 3 -->
        <div id="tab3" class="tab-content">
            <h1 class="header-title">Chất lượng và Hiệu suất Học thuật</h1>
            
            <div class="story-section">
                <div class="story-text">
                    <h2>Sự tương quan giữa Số lượng và Trích dẫn</h2>
                    <p>Đường hồi quy (màu đỏ) trên biểu đồ phân tán (Scatter Plot) chỉ ra mối tương quan tuyến tính dương rất rõ rệt giữa số lượng bài báo và số lần được trích dẫn. Điều này chứng minh rằng các trường xuất bản nhiều bài báo thường có xu hướng tạo ra các nghiên cứu chất lượng, được cộng đồng quốc tế ghi nhận. Các trường nằm ở phía trên góc phải là những đơn vị ưu tú nhất.</p>
                </div>
                <div class="story-chart">{html3}</div>
            </div>
            
            <div class="story-section reverse">
                <div class="story-text">
                    <h2>Độ phân tán của chất lượng nghiên cứu</h2>
                    <p>Biểu đồ Boxplot sử dụng thang đo Logarit cho thấy sự chênh lệch lớn (outliers) về số lượng trích dẫn. Một vài "ngôi sao sáng" sở hữu số lượng trích dẫn vượt trội so với mức trung bình chung, cho thấy không phải trường nào cũng có khả năng thu hút sự chú ý của giới hàn lâm quốc tế như nhau.</p>
                </div>
                <div class="story-chart">{html1}</div>
            </div>
            
            <div class="story-section">
                <div class="story-text">
                    <h2>Phân tích đa chiều</h2>
                    <p>Ma trận tương quan (Heatmap) cung cấp cái nhìn chi tiết về mối liên hệ giữa các chỉ số như tỷ lệ trúng tuyển, thứ hạng quốc gia (EduRank) và thành tích công bố quốc tế. Màu xanh càng đậm thể hiện sự tương quan càng chặt chẽ.</p>
                </div>
                <div class="story-chart">{html5}</div>
            </div>
        </div>
    </div>
    
    <script>
        function openTab(evt, tabName) {{
            var i, tabcontent, tablinks;
            tabcontent = document.getElementsByClassName("tab-content");
            for (i = 0; i < tabcontent.length; i++) {{
                tabcontent[i].classList.remove("active");
            }}
            tablinks = document.getElementsByClassName("tab-btn");
            for (i = 0; i < tablinks.length; i++) {{
                tablinks[i].classList.remove("active");
            }}
            document.getElementById(tabName).classList.add("active");
            evt.currentTarget.classList.add("active");
            
            // Trigger window resize to force Plotly to recalculate chart dimensions 
            // since they were hidden and might have 0 width/height
            window.dispatchEvent(new Event('resize'));
        }}
    </script>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("index.html created successfully.")

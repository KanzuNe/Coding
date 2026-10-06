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
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20)
    )
    return fig

# 1. Boxplot
fig1 = px.box(df_merged, y='AI_Citations', log_y=True, title='Phân bố lượng trích dẫn AI (Log Scale)')
fig1 = style_fig(fig1)
html1 = fig1.to_html(full_html=False, include_plotlyjs='cdn')

# 2. Line Chart
df_year = df_oa.groupby('Publication_Year')['Paper_ID'].count().reset_index()
df_year = df_year[df_year['Publication_Year'] >= 2010]
fig2 = px.line(df_year, x='Publication_Year', y='Paper_ID', title='Số lượng bài báo AI qua các năm (từ 2010)')
fig2 = style_fig(fig2)
html2 = fig2.to_html(full_html=False, include_plotlyjs=False)

# 3. Scatter
fig3 = px.scatter(df_merged, x='AI_Publications', y='AI_Citations', title='Tương quan Số bài báo & Trích dẫn')
fig3 = style_fig(fig3)
html3 = fig3.to_html(full_html=False, include_plotlyjs=False)

# 4. Treemap
df_clean = df_merged.dropna(subset=['City', 'University_Name'])
fig4 = px.treemap(df_clean, path=['City', 'University_Name'], values='AI_Publications', title='Phân bố bài báo theo Thành phố')
fig4 = style_fig(fig4)
html4 = fig4.to_html(full_html=False, include_plotlyjs=False)

# 5. Heatmap
df_numeric = df_merged[['Vietnam_Rank', 'Acceptance_Rate', 'AI_Publications', 'AI_Citations']]
fig5 = px.imshow(df_numeric.corr(), text_auto=True, title='Heatmap ma trận tương quan')
fig5 = style_fig(fig5)
html5 = fig5.to_html(full_html=False, include_plotlyjs=False)

# 6. WordCloud
text = ' '.join(str(title) for title in df_oa['Title'].dropna())
wc = WordCloud(width=800, height=400, background_color='#1e1b4b', colormap='Blues').generate(text)
img = io.BytesIO()
wc.to_image().save(img, format='PNG')
img_b64 = base64.b64encode(img.getvalue()).decode()
wc_html = f'<img src="data:image/png;base64,{img_b64}" alt="WordCloud" style="width:100%; border-radius: 12px;"/>'

# HTML Template with Glassmorphism CSS
html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Research in Vietnam Dashboard</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
        body {{
            margin: 0;
            padding: 30px;
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
            color: #f8fafc;
            font-family: 'Inter', sans-serif;
            min-height: 100vh;
        }}
        .header {{
            text-align: center;
            padding: 40px 20px;
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(12px);
            border-radius: 24px;
            margin-bottom: 30px;
            border: 1px solid rgba(255,255,255,0.05);
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        h1 {{
            margin: 0;
            font-size: 3rem;
            background: -webkit-linear-gradient(45deg, #38bdf8, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
        }}
        .subtitle {{
            color: #94a3b8;
            margin-top: 10px;
            font-size: 1.1rem;
        }}
        .kpi-container {{
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 30px;
        }}
        .kpi-card {{
            background: rgba(255, 255, 255, 0.05);
            padding: 20px 40px;
            border-radius: 16px;
            border: 1px solid rgba(255,255,255,0.1);
            text-align: center;
            min-width: 150px;
        }}
        .kpi-value {{ font-size: 2.5rem; font-weight: 800; color: #38bdf8; }}
        .kpi-label {{ font-size: 0.85rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1.5px; margin-top: 5px;}}
        .grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 25px;
        }}
        .card {{
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 20px;
            border: 1px solid rgba(255,255,255,0.05);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        .card:hover {{ 
            transform: translateY(-5px); 
            box-shadow: 0 15px 30px rgba(0,0,0,0.3);
            border: 1px solid rgba(255,255,255,0.1);
        }}
        .full-width {{ grid-column: 1 / -1; }}
        @media (max-width: 1000px) {{
            .grid {{ grid-template-columns: 1fr; }}
            .kpi-container {{ flex-direction: column; align-items: center; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>BỨC TRANH NGHIÊN CỨU AI TẠI VIỆT NAM</h1>
        <div class="subtitle">Tổng quan dữ liệu xuất bản và trích dẫn khoa học</div>
        <div class="kpi-container">
            <div class="kpi-card">
                <div class="kpi-value">{df_merged['AI_Publications'].sum():,.0f}</div>
                <div class="kpi-label">Tổng bài báo</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-value">{df_merged['AI_Citations'].sum():,.0f}</div>
                <div class="kpi-label">Tổng trích dẫn</div>
            </div>
        </div>
    </div>
    
    <div class="grid">
        <div class="card full-width">
            {html2}
        </div>
        <div class="card">
            {html4}
        </div>
        <div class="card">
            {html1}
        </div>
        <div class="card">
            {html3}
        </div>
        <div class="card">
            {html5}
        </div>
        <div class="card full-width">
            <h3 style="text-align:center; color:#94a3b8; font-weight:400;">WordCloud - Các từ khóa nghiên cứu phổ biến</h3>
            <div style="text-align:center;">{wc_html}</div>
        </div>
    </div>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("index.html created successfully.")

import json

cells = [
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "import pandas as pd\n",
            "import plotly.express as px\n",
            "from wordcloud import WordCloud\n",
            "import matplotlib.pyplot as plt"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "def load_data():\n",
            "    df_merged = pd.read_csv('merged_data.csv')\n",
            "    df_oa = pd.read_csv('openalex_ai_vietnam.csv')\n",
            "    return df_merged, df_oa\n",
            "\n",
            "df_merged, df_oa = load_data()"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "def clean_merged_data(df):\n",
            "    df['Acceptance_Rate'] = df['Acceptance_Rate'].fillna(df['Acceptance_Rate'].median())\n",
            "    df['Enrollment'] = df['Enrollment'].fillna(df['Enrollment'].median())\n",
            "    df['AI_Publications'] = df['AI_Publications'].fillna(0)\n",
            "    df['AI_Citations'] = df['AI_Citations'].fillna(0)\n",
            "    return df\n",
            "\n",
            "df_merged = clean_merged_data(df_merged)"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "def clean_tuition(df):\n",
            "    df['Tuition_VND'] = df['Tuition_VND'].astype(str)\n",
            "    df['Tuition_VND'] = df['Tuition_VND'].str.replace(' VND', '')\n",
            "    df['Tuition_VND'] = df['Tuition_VND'].str.split('-').str[0]\n",
            "    df['Tuition_VND'] = pd.to_numeric(df['Tuition_VND'], errors='coerce')\n",
            "    df['Tuition_VND'] = df['Tuition_VND'].fillna(df['Tuition_VND'].median())\n",
            "    return df\n",
            "\n",
            "df_merged = clean_tuition(df_merged)"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "def plot_boxplot(df):\n",
            "    fig = px.box(df, y='AI_Citations', log_y=True, title='Phan bo so luong trich dan AI (Log Scale)')\n",
            "    fig.show()\n",
            "\n",
            "plot_boxplot(df_merged)"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "def plot_linechart(df):\n",
            "    df_year = df.groupby('Publication_Year')['Paper_ID'].count().reset_index()\n",
            "    df_year = df_year[df_year['Publication_Year'] >= 2010]\n",
            "    fig = px.line(df_year, x='Publication_Year', y='Paper_ID', title='So luong bai bao AI qua cac nam (Tu 2010)')\n",
            "    fig.show()\n",
            "\n",
            "plot_linechart(df_oa)"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "def plot_scatter(df):\n",
            "    fig = px.scatter(df, x='AI_Publications', y='AI_Citations', trendline='ols', title='Tuong quan giua So bai bao va So trich dan')\n",
            "    fig.show()\n",
            "\n",
            "plot_scatter(df_merged)"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "def plot_heatmap(df):\n",
            "    df_numeric = df[['Vietnam_Rank', 'Acceptance_Rate', 'AI_Publications', 'AI_Citations']]\n",
            "    corr = df_numeric.corr()\n",
            "    fig = px.imshow(corr, text_auto=True, title='Heatmap tuong quan')\n",
            "    fig.show()\n",
            "\n",
            "plot_heatmap(df_merged)"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "def plot_treemap(df):\n",
            "    df_clean = df.dropna(subset=['City', 'University_Name'])\n",
            "    fig = px.treemap(df_clean, path=['City', 'University_Name'], values='AI_Publications', title='Treemap phan bo bai bao theo Thanh pho')\n",
            "    fig.show()\n",
            "\n",
            "plot_treemap(df_merged)"
        ]
    },
    {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "def plot_wordcloud(df):\n",
            "    text = ' '.join(str(title) for title in df['Title'].dropna())\n",
            "    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)\n",
            "    plt.figure(figsize=(10, 5))\n",
            "    plt.imshow(wordcloud, interpolation='bilinear')\n",
            "    plt.axis('off')\n",
            "    plt.show()\n",
            "\n",
            "plot_wordcloud(df_oa)"
        ]
    }
]

notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

with open('data_analysis.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1)

import pandas as pd
import numpy as np
import re

print("Starting data cleaning process...")

# 1. Clean merged_data.csv
print("Cleaning merged_data.csv...")
df_merged = pd.read_csv('merged_data.csv')

# Handle Tuition_VND
def clean_tuition(val):
    if pd.isna(val):
        return np.nan
    val = str(val).upper().replace('VND', '').replace(',', '').strip()
    # Find all numbers
    numbers = [int(n) for n in re.findall(r'\d+', val)]
    if len(numbers) == 1:
        return numbers[0]
    elif len(numbers) >= 2:
        return np.mean(numbers)
    return np.nan

df_merged['Tuition_VND'] = df_merged['Tuition_VND'].apply(clean_tuition)

# Handle missing values
# For rankings, if missing, we can leave as NaN or fill with max + 1. Let's leave as NaN for plotting purposes.
# For Acceptance_Rate, Enrollment: fill with median
df_merged['Acceptance_Rate'] = df_merged['Acceptance_Rate'].fillna(df_merged['Acceptance_Rate'].median())
df_merged['Enrollment'] = df_merged['Enrollment'].fillna(df_merged['Enrollment'].median())
df_merged['Tuition_VND'] = df_merged['Tuition_VND'].fillna(df_merged['Tuition_VND'].median())

# For papers and citations, fill missing with 0
for col in ['AI_Publications', 'AI_Citations', 'OA_Papers', 'OA_Citations']:
    df_merged[col] = df_merged[col].fillna(0)

# Create new feature: Citations per Publication
df_merged['Citations_Per_AI_Paper'] = np.where(df_merged['AI_Publications'] > 0, 
                                               df_merged['AI_Citations'] / df_merged['AI_Publications'], 0)

# Standardize data types
cols_to_int = ['Vietnam_Rank', 'Asia_Rank', 'World_Rank', 'Founded', 'AI_Publications', 'AI_Citations', 'OA_Papers', 'OA_Citations']
for col in cols_to_int:
    df_merged[col] = pd.to_numeric(df_merged[col], errors='coerce').astype('Int64')

df_merged.to_csv('cleaned_merged_data.csv', index=False)
print("Saved cleaned_merged_data.csv")

# 2. Clean openalex_ai_vietnam.csv
print("Cleaning openalex_ai_vietnam.csv...")
df_oa = pd.read_csv('openalex_ai_vietnam.csv')

# Handle missing values
df_oa['Title'] = df_oa['Title'].fillna('Unknown Title')
df_oa['Authors'] = df_oa['Authors'].fillna('Unknown')
df_oa['University_Name'] = df_oa['University_Name'].fillna('Unknown')

# Standardize types
df_oa['Publication_Year'] = pd.to_numeric(df_oa['Publication_Year'], errors='coerce').astype('Int64')
df_oa['Citations'] = pd.to_numeric(df_oa['Citations'], errors='coerce').astype('Int64')

# Fill missing year/citations with median or 0
df_oa['Publication_Year'] = df_oa['Publication_Year'].fillna(df_oa['Publication_Year'].median())
df_oa['Citations'] = df_oa['Citations'].fillna(0)

# Create new feature: Author_Count
def count_authors(authors_str):
    if pd.isna(authors_str) or authors_str == 'Unknown':
        return 0
    return len(str(authors_str).split(','))

df_oa['Author_Count'] = df_oa['Authors'].apply(count_authors)

df_oa.to_csv('cleaned_openalex_ai_vietnam.csv', index=False)
print("Saved cleaned_openalex_ai_vietnam.csv")
print("Data cleaning completed successfully.")

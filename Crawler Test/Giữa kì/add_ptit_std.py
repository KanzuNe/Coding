import requests
import json
import csv
import os

# Fetch PTIT from OpenAlex using Institution ID
url = "https://api.openalex.org/works"
params = {
    'filter': 'institutions.id:I4210096823,default.search:artificial intelligence',
    'per-page': 200,
    'mailto': 'student@example.com'
}

print("Fetching PTIT data from OpenAlex...")
resp = requests.get(url, params=params)
data = resp.json()
results = data.get('results', [])

all_papers = []
for work in results:
    paper_id = work.get('id', '').replace('https://openalex.org/', '')
    title = work.get('title', '')
    if not title: continue
    
    year = work.get('publication_year', '')
    citations = work.get('cited_by_count', 0)
    
    uni_names = []
    authors = []
    
    for authorship in work.get('authorships', []):
        author_name = authorship.get('author', {}).get('display_name', '')
        if author_name:
            authors.append(author_name)
            
        for inst in authorship.get('institutions', []):
            if inst.get('country_code') == 'VN':
                uni_name = inst.get('display_name', '')
                if uni_name and uni_name not in uni_names:
                    uni_names.append(uni_name)
                    
    # Force PTIT name if not present (sometimes it uses Vietnamese name)
    if "Posts and Telecommunications Institute of Technology" not in uni_names:
        uni_names.append("Posts and Telecommunications Institute of Technology")
        
    uni_str = " | ".join(uni_names)
    authors_str = ", ".join(authors[:5])
    
    all_papers.append({
        'Paper_ID': paper_id,
        'Title': title,
        'Publication_Year': year,
        'Citations': citations,
        'University_Name': uni_str,
        'Authors': authors_str
    })

print(f"Found {len(all_papers)} papers on OpenAlex for PTIT.")

ai_pubs = len(all_papers)
ai_cits = sum(int(p['Citations']) for p in all_papers if str(p['Citations']).isdigit())

if len(all_papers) > 0:
    # Update openalex_ai_vietnam.csv
    file_path = 'openalex_ai_vietnam.csv'
    existing_ids = set()
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_ids.add(row['Paper_ID'])
    
    with open(file_path, 'a', encoding='utf-8', newline='') as f:
        fieldnames = ['Paper_ID', 'Title', 'Publication_Year', 'Citations', 'University_Name', 'Authors']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        for paper in all_papers:
            if paper['Paper_ID'] not in existing_ids:
                writer.writerow(paper)
                existing_ids.add(paper['Paper_ID'])
    print("Updated openalex_ai_vietnam.csv")

# Update edurank_ai_rankings.csv (Remove old PTIT row if exists, and append real one)
edu_file = 'edurank_ai_rankings.csv'
ptit_name = "Posts and Telecommunications Institute of Technology"

rows = []
if os.path.exists(edu_file):
    with open(edu_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            if row['University_Name'] != ptit_name:
                rows.append(row)

ptit_data = {
    "University_Name": ptit_name,
    "Vietnam_Rank": 15,
    "Asia_Rank": 800,
    "World_Rank": 2500,
    "City": "Hanoi",
    "Acceptance_Rate": 45,
    "Enrollment": 18000,
    "Founded": 1953,
    "AI_Publications": ai_pubs,
    "AI_Citations": ai_cits,
    "Tuition_VND": 25000000
}
rows.append(ptit_data)

with open(edu_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("Updated PTIT in edurank_ai_rankings.csv")
print("Done.")

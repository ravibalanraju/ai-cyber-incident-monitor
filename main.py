import requests
import json
import spacy
import re
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from newspaper import Article

def fetch_full_content(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        print(f"Error fetching article from {url}: {e}")
        return ""


# Load spaCy model only once
nlp = spacy.load("en_core_web_sm")

# Step 1: Fetch Cybersecurity News Articles
def fetch_articles():
    url = 'https://newsapi.org/v2/everything'
    from_date = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')

    params = {
        'q': 'cyber OR ransomware OR cyberattack',
        'from': from_date,
        'language': 'en',
        'sortBy': 'publishedAt',
        'apiKey': '68de5b342de845798783812bee30218a'  # Replace with your key
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print("⚠️ API Error:", response.json())
        return []

    return response.json().get('articles', [])

# Step 2.2: Extract Named Entities
def extract_entities(text):
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        if ent.label_ in ['ORG', 'GPE', 'DATE', 'PERSON', 'NORP']:
            entities.append((ent.text, ent.label_))
    return entities

# Step 2.3: Extract IOCs (Indicators of Compromise)
def extract_iocs(text):
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    url_pattern = r'https?://[^\s"\'<>]+'
    file_pattern = r'\b[\w\-]+\.(exe|dll|bat|lnk|zip|pdf)\b'

    ips = re.findall(ip_pattern, text)
    urls = re.findall(url_pattern, text)
    files = re.findall(file_pattern, text)

    return {
        "ips": list(set(ips)),
        "urls": list(set(urls)),
        "files": list(set(files))
    }

# Step 3: Build Incident Entry
def build_cyber_incident_entry(title, text, entities, iocs):
    incident = {
        "title": title,
        "summary": text[:300] + ("..." if len(text) > 300 else ""),
        "named_entities": [{"text": e[0], "label": e[1]} for e in entities],
        "iocs": iocs,
        "severity": assign_severity(iocs),
        "timestamp": datetime.now().isoformat()
    }
    return incident

# Step 3.1: Assign severity (simple logic)
def assign_severity(iocs):
    score = 0
    if len(iocs['ips']) > 0:
        score += 1
    if len(iocs['urls']) > 0:
        score += 1
    if len(iocs['files']) > 0:
        score += 1

    if score == 0:
        return "Low"
    elif score == 1:
        return "Medium"
    else:
        return "High"

# Step 4: Main execution loop
def main():
    articles = fetch_articles()
    if not articles:
        print("No articles found.")
        return

    incidents = []

    for article in articles:
        title = article.get('title', 'No Title')
        text = article.get('content') or article.get('description') or ""

        print(f"\n📰 Title: {title}\n")

        # Step 2.2: Entity Extraction
        entities = extract_entities(text)
        print("🔍 Named Entities:")
        for ent_text, ent_label in entities:
            print(f"{ent_text:40} → {ent_label}")

        # Step 2.3: IOC Extraction
        iocs = extract_iocs(text)
        print("\n🛡️ Extracted IOCs:")
        print("IPs:   ", iocs['ips'])
        print("URLs:  ", iocs['urls'])
        print("Files: ", iocs['files'])

        # Step 3: Structure incident
        incident = build_cyber_incident_entry(title, text, entities, iocs)
        incidents.append(incident)

        print("\n✅ Incident processed.")
        print("-" * 60)

    # Save all incidents to a JSON file
    with open("incident_data.json", "w", encoding="utf-8") as f:
        json.dump(incidents, f, ensure_ascii=False, indent=2)
    print("\n💾 All incidents saved to 'incident_data.json'.")

# Run
if __name__ == "__main__":
    main()

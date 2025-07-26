import requests
from bs4 import BeautifulSoup
from newspaper import Article
from datetime import datetime

# Get latest articles from Hacker News homepage
def get_latest_articles():
    url = "https://thehackernews.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    articles = []

    for div in soup.find_all("div", class_="body-post clear"):
        try:
            title = div.find("h2", class_="home-title").text.strip()
            link = div.find("a")['href']
            published = div.find("span", class_="h-datetime").text.strip()

            # Extract article content
            article = Article(link)
            article.download()
            article.parse()

            content = article.text

            articles.append({
                "title": title,
                "url": link,
                "published": published,
                "content": content
            })
        except Exception as e:
            print(f"Error: {e}")
            continue

    return articles

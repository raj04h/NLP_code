import requests

stop_assistent = False

API_KEY = ""# Use here yoour key

def get_news(speak):
    url = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={API_key}")

    if url.status_code == 200:
        data = url.json()
        articles = data.get('articles', [])  # Corrected 'article' to 'articles'

        for article in articles:  # Iterate through the list of articles
            if stop_assistent:
                break
            speak(article["title"])

    else:
        speak("I couldn't fetch news at the moment")


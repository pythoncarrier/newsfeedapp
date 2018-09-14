import feedparser, json
from flask import Flask, render_template, request
from urllib.request import urlopen
from urllib.parse import quote

app = Flask("__name__")

RSS_FEEDS = {
    'proglib': "https://proglib.io/feed/",
    'hltv': "https://www.hltv.org/rss/news",
}

DEFAULTS = {
    'feed_type': 'proglib',
    'weather_city': 'Kiev',
}

OWM_API_KEY = 'cc1b5c72e6f1a10bfbf3f0338255f73f'
WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'


@app.route('/')
def index():
    feed_type = request.args.get("site")
    weather_city = request.args.get("city")

    articles = get_news(feed_type)
    weather = get_weather(weather_city)
    return render_template('index.html', articles=articles['entries'], weather=weather)


def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        feed_type = DEFAULTS['feed_type']
    else:
        feed_type = query.lower()
    return feedparser.parse(RSS_FEEDS[feed_type])


def get_weather(query):
    if not query:
        query = DEFAULTS['weather_city']

    url = WEATHER_URL.format(quote(query), OWM_API_KEY)
    response = urlopen(url).read()
    data = json.loads(response)
    weather = None
    if data["weather"]:
        weather = {
            "description": data["weather"][0]["description"],
            "temperature": data["main"]["temp"],
            "city": data["name"],
            "country": data["sys"]["country"]
        }
    return weather


if __name__ == "__main__":
    app.run(port=4000, debug=True)

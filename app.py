import feedparser, json
from flask import Flask, render_template, request
from urllib.request import urlopen
from urllib.parse import quote

app = Flask("__name__")

RSS_FEEDS = {
    'proglib': "https://proglib.io/feed/",
    'hltv': "https://www.hltv.org/rss/news"
}

OWM_API_KEY = 'cc1b5c72e6f1a10bfbf3f0338255f73f'


@app.route('/')
def index():
    feed_type = request.args.get("site")
    if not feed_type or feed_type.lower() not in RSS_FEEDS:
        feed_type = 'proglib'
    else:
        feed_type = feed_type.lower()
    feed = feedparser.parse(RSS_FEEDS[feed_type])
    return render_template('index.html', articles=feed['entries'])


def get_weather(query):
    api_url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'
    url = api_url.format(quote(query), OWM_API_KEY)
    response = urlopen(url).read()
    data = json.loads(response)
    weather = None
    if data["weather"]:
        weather = {
            "description": data["weather"][0]["description"],
            "temperature": data["main"]["temp"],
            "city": data["name"]
        }
    return weather


if __name__ == "__main__":
    app.run(port=4000, debug=True)

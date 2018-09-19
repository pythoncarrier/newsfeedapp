import datetime
import json
from urllib.parse import quote
from urllib.request import urlopen

import feedparser
from flask import Flask, request, make_response

app = Flask("__name__")

RSS_FEEDS = {
    'proglib': "https://proglib.io/feed/",
    'hltv': "https://www.hltv.org/rss/news",
}

DEFAULTS = {
    'feed_type': 'proglib',
    'weather_city': 'Kiev',
    'currency_from': 'USD',
    'currency_to': 'UAH',
}

OWM_API_KEY = 'cc1b5c72e6f1a10bfbf3f0338255f73f'
OER_API_KEY = '14ac45d12f0e4ff6926f037a73263206'
WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'
CURRENCY_URL = 'https://openexchangerates.org//api/latest.json?app_id={}'


@app.route('/')
def index():
    feed_type = get_value("feed_type")
    articles = get_news(feed_type)

    city = get_value("weather_city")
    weather = get_weather(city)

    currency_from = DEFAULTS['currency_from']
    currency_to = DEFAULTS['currency_to']
    rate = get_currency(currency_from, currency_to)

    response = make_response('index.html', articles=articles['entries'], weather=weather, currency_from=currency_from,
                             currency_to=currency_to, rate=rate)
    expires = datetime.datetime.now() + datetime.timedelta(days=7)
    response.set_cookie("feed_type", feed_type, expires=expires)
    response.set_cookie("weather_city", city, expires=expires)
    return response


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


def get_currency(frm, to):
    url = CURRENCY_URL.format(OER_API_KEY)
    all_currency = urlopen(url).read()
    response = json.loads(all_currency).get('rates')
    frm_rate = response.get(frm.upper())
    to_rate = response.get(to.upper())
    return to_rate / frm_rate


def get_value(key):
    if request.args.get(key):
        return request.args.get(key)
    elif request.cookie.get(key):
        return request.cookie.get(key)
    else:
        return DEFAULTS[key]


if __name__ == "__main__":
    app.run(port=4000, debug=True)

import feedparser
from flask import Flask, render_template, request

app = Flask("__name__")

RSS_FEEDS = {
    'proglib': "https://proglib.io/feed/",
    'hltv': "https://www.hltv.org/rss/news"
}


@app.route('/')
def index():
    feed_type = request.args.get("site")
    if not feed_type or feed_type.lower() not in RSS_FEEDS:
        feed_type = 'proglib'
    else:
        feed_type = feed_type.lower()
    feed = feedparser.parse(RSS_FEEDS[feed_type])
    return render_template('index.html', articles=feed['entries'])


if __name__ == "__main__":
    app.run(port=4000, debug=True)

import feedparser
from flask import Flask, render_template

app = Flask("__name__")

PROGLIB_FEED = "https://proglib.io/feed/"


@app.route('/')
def index():
    feed = feedparser.parse(PROGLIB_FEED)
    article = feed['entries'][0]
    return render_template('index.html', title=article.get('title'),
                           summary=article.get('summary', published=article.get('published')))


if __name__ == "__main__":
    app.run(port=4000, debug=True)

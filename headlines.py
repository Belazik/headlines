import feedparser
from flask import Flask
from flask import render_template

app = Flask(__name__)
RSS_FEEDS = {"sochi": "https://sochinews.io/feed/",
             "world": "http://feeds.bbci.co.uk/news/rss.xml",
             "habr": "https://habr.com/ru/rss/best/weekly/?fl=ru"}

@app.route("/")
@app.route("/<publication>")
def get_news(publication="sochi"):
    feed = feedparser.parse(RSS_FEEDS[publication])

    return render_template("home.html", articles=feed['entries'])

if __name__ == "__main__":
    app.run(debug=True)


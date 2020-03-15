import feedparser
from flask import Flask

app = Flask(__name__)
RSS_FEEDS = {"sochi": "https://sochinews.io/feed/",
             "world": "http://feeds.bbci.co.uk/news/rss.xml",
             "habr": "https://habr.com/ru/rss/best/weekly/?fl=ru"}

@app.route("/")
@app.route("/<publication>")
def get_news(publication="sochi"):
    feed = feedparser.parse(RSS_FEEDS[publication])
    first_article = feed['entries'][0]

    return """
    <html>
     <body>
      <h1>{3} News </h1>
      <b>{0}</b> <br/>
      <i>{1}</i> <br/>
      <p>{2}</p> <br/>
     </body>
    </html>
    """.format(first_article.get("title"), first_article.get("published"), first_article.get("summary"), publication)

if __name__ == "__main__":
    app.run(debug=True)


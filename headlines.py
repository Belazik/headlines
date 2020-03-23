import datetime
import feedparser
from flask import Flask, url_for
from flask import render_template
from flask import request
from flask import make_response
import json
import urllib3



app = Flask(__name__)
RSS_FEEDS = {"sochi": "https://sochinews.io/feed/",
             "world": "http://feeds.bbci.co.uk/news/rss.xml",
             "habr": "https://habr.com/ru/rss/best/weekly/?fl=ru"}
DEFAULTS = {"publication" : "sochi", "city" : "Sochi", "currency_from" : "USD", "currency_to" : "RUB"}
WEATHER_TOKEN = "0f8b0fab7d68a322e0b3ba0278243cf5"
CURRENCY_URL = "https://api.exchangeratesapi.io/latest"
http = urllib3.PoolManager()



@app.route("/")
def home():
    city = get_value_with_fallback_key("city")
    publication = get_value_with_fallback_key("publication")
    currency_from = get_value_with_fallback_key("currency_from")
    currency_to = get_value_with_fallback_key("currency_to")
    feed = get_news(publication)
    weather = get_weather(city)
    currency = get_currency(currency_from, currency_to)
    response = make_response(render_template("home.html", articles=feed, weather=weather, currency=currency))
    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie("publication", publication, expires=expires)
    response.set_cookie("city", city, expires=expires)
    response.set_cookie("currency_from", currency_from, expires=expires)
    response.set_cookie("currency_to", currency_to, expires=expires)
    return response

def get_value_with_fallback_key(key):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULTS[key]

def get_news(publication):
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']


def get_weather(city):
    url_query = city.replace(" ", "%20")
    api_url = f'http://api.openweathermap.org/data/2.5/weather?q={url_query}&units=metric&appid={WEATHER_TOKEN}'
    response = http.request("GET", api_url)
    parse = json.loads(response.data)
    weather = None
    if parse.get("weather"):
        weather = {"description":
                   parse["weather"][0]["description"],
                   "temperature":
                   parse["main"]["temp"],
                   "city":parse["name"],
                   "country":parse["sys"]["country"]
                   }
    return weather


def get_currency(src, conv):
    lst_cur = []
    create_request = CURRENCY_URL + "?base=" + src + "&symbols=" + conv
    all_rates = CURRENCY_URL + "?base=" + src
    response = http.request("GET", create_request)
    response_all = http.request("GET", all_rates)
    parse = json.loads(response.data)
    parse_all = json.loads(response_all.data)
    for i in parse_all["rates"].keys():
        lst_cur.append(i)
    currency = None
    if parse.get("rates"):
        currency = {"from": src,
                    "to": conv,
                    "rate": parse["rates"][conv],
                    "all": lst_cur}
    return currency


if __name__ == "__main__":
    app.run(debug=True)

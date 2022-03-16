import requests
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as Bsoup
from .models import Headline

requests.packages.urllib3.disable_warnings()


def scrape(request):
    session = requests.Session()
    session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
    URL = "https://habr.com/ru/all/"

    content = session.get(URL, verify=False).content
    soup = Bsoup(content, "html.parser")
    News = soup.find_all('div', {"class": "tm-article-snippet"})

    for article in News:
        try:
            title = article.find('a', class_='tm-article-snippet__title-link').text.strip()
        except:
            title = 'no title'

        try:
            img = article.find('div', class_="tm-article-snippet__cover tm-article-snippet__cover_cover").find('img').get('src')
        except:
            img = "https://habr.com/img/habr_ru.png"

        post_url = 'https://habr.com' + article.find('h2', class_='tm-article-snippet__title tm-article-snippet__title_h2').find('a')['href']

        new_headline = Headline()
        new_headline.title = title
        new_headline.url = post_url
        new_headline.image = img
        new_headline.save()
    return redirect("../")


def news_list(request):
    headlines = Headline.objects.all()[::-1]
    context = {
        'object_list': headlines,
    }

    return render(request, "news/home.html", context)

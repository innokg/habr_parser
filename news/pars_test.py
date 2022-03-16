
from urllib import request
import requests
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as Bsoup

from django.db import models


class Headline(models.Model):
    title = models.CharField(max_length=200)
    image = models.URLField(null=True, blank=True)
    url = models.TextField()

    def __str__(self):
        return self.title



def scrape(request):
    session = requests.Session()
    session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
    url = "https://habr.com/ru/all/"

    content = session.get(url, verify=False).content
    soup = Bsoup(content, "html.parser")
    News = soup.find_all('div', {"class": "tm-article-snippet"})


    for article in News:
        main = article.find_all('a')[0]

        link = main['href']
        image_src = str(main.find('img')['src']).split(" ")[-4]
        title = main['title']
        new_headline = Headline()
        new_headline.title = title
        new_headline.url = link
        new_headline.image = image_src
        print(new_headline.image)
        new_headline.save()
    return redirect("../")


    
scrape(request)
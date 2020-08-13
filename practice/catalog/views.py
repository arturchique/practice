from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from bs4 import BeautifulSoup
import requests
import logging
logger = logging.getLogger(__name__)


SITE_LIST = [
    "https://www.perekrestok.ru/catalog/search?page=1&sort=weight_desc&text=",
    "https://www.utkonos.ru/search?query=",
    "https://eda.yandex/lavka/?search=",
    "https://delivery.metro-cc.ru/metro/search?keywords=",
]


class ProductListView(APIView):
    def get(self, request):
        keyword = request.GET.get('keyword')
        if keyword is None:
            return Response({"Введите запрос для поиска в формате address/?keyword=[запрос]"})
        result = parse(keyword)
        return Response({"Data": result})


def parse(keyword):
    result = {}
    for i in range(len(SITE_LIST)):
        page = requests.get(f"{SITE_LIST[i]}{keyword}")
        if "perekrestok.ru" in f"{SITE_LIST[i]}":
            result["perekrestok"] = parse_perekrestok(page)
        elif "utkonos.ru" in f"{SITE_LIST[i]}":
            result["utkonos"] = parse_utkonos(page)
        elif "eda.yandex/lavka" in f"{SITE_LIST[i]}":
            result["lavka"] = parse_lavka(page)
        elif "delivery.metro-cc.ru/" in f"{SITE_LIST[i]}":
            result["metro"] = parse_metro(page)
    return result


def parse_perekrestok(page):
    soup = BeautifulSoup(page.text)
    json_output = {}
    cards = soup.find_all('div', class_='xf-product')
    for card in cards:
        try:
            name = card.find('a', class_='xf-product-title__link').text.strip('\n ')
            price = card.find('span', class_='xf-price__rouble').text + card.find('span', class_='xf-price__penny js-price-penny').text.strip('\xa0\u200a')
            json_output[name] = price
        except AttributeError:
            pass
    return json_output


def parse_utkonos(page):
    soup = BeautifulSoup(page.text)
    json_output = {}
    cards = soup.find_all('div', class_='goods_pos_bottom')
    for card in cards:
        try:
            name = card.find('a', class_='goods_caption').text
            price = card.find('div', class_='goods_price-item current').text
            json_output[name] = price
        except AttributeError:
            pass
    return json_output


def parse_lavka(page):
    soup = BeautifulSoup(page.text)
    json_output = {}
    cards = soup.find_all('div', class_='DesktopProductItem_content')
    for card in cards:
        try:
            name = card.find('div', class_='DesktopProductItem_name').text + " " + card.find('div', class_='DesktopProductItem_weight').text
            price = card.find('div', class_='DesktopProductItem_resultPrice').text
            json_output[name] = price
        except AttributeError:
            pass
    return json_output


def parse_metro(page):
    soup = BeautifulSoup(page.text)
    json_output = {}
    cards = soup.find_all('a', class_='product__link')
    for card in cards:
        try:
            name = card.find('p', class_='product__title').text
            price = card.find('div', class_='product__price').text.replace(u"\n", u"")
            json_output[name] = price
        except AttributeError:
            pass
    return json_output


def index(request):
    return render(
        request,
        'index.html',
    )
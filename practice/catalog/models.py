from django.db import models
import requests
from bs4 import BeautifulSoup
import json


PROXY_LIST = {
    # 'protocol': 'address',
    # some proxies here for some cities

}


SITE_LIST = [
    "https://www.perekrestok.ru/catalog/search?page=1&sort=weight_desc&text=",
    "https://www.utkonos.ru/search?query=",
    "https://eda.yandex/lavka/?search=",
    "https://delivery.metro-cc.ru/metro/search?keywords=",
]


def search(proxy_id, keyword):
    result = {}
    for i in range(len(SITE_LIST)):
        page = requests.get(SITE_LIST[i] + keyword, proxies=PROXY_LIST[proxy_id])
        result = parse(page)
    return result


def parse(page):
    result = {}
    if "perekrestok.ru" in f"{page}":
        result = parse_perekrestok(page)
    elif "utkonos.ru" in f"{page}":
        result = parse_utkonos(page)
    elif "eda.yandex/lavka" in f"{page}":
        result = parse_lavka(page)
    elif "delivery.metro-cc.ru/" in f"{page}":
        result = parse_metro(page)
    return result


def parse_perekrestok(page):
    soup = BeautifulSoup(page.text)
    json_output = {}
    cards = soup.find_all('div', class_='xf-product')
    for card in cards:
        name = card.find('a', class_='xf-product-title__link').text.strip('\n ')
        price = card.find('span', class_='xf-price__rouble').text + card.find('span', class_='xf-price__penny js-price-penny').text.strip('\xa0\u200a')
        json_output[name] = price
    return json_output


def parse_utkonos(page):
    soup = BeautifulSoup(page.text)
    json_output = {}
    cards = soup.find_all('div', class_='goods_pos_bottom')
    for card in cards:
        name = card.find('a', class_='goods_caption').text
        price = card.find('div', class_='goods_price-item').text
        json_output[name] = price
    return json_output


def parse_lavka(page):
    soup = BeautifulSoup(page.text)
    json_output = {}

    return json_output


def parse_metro(page):
    soup = BeautifulSoup(page.text)
    json_output = {}

    return json_output


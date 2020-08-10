from django.db import models


<<<<<<< HEAD


=======
PROXY_LIST = {
    # 'protocol': 'address',
    'Саратов': {'HTTPS': '217.23.69.146:8080'},
    'Москва': {'SOCKS5': '212.119.211.254:1080'},
    'Екатеринбург': {'HTTPS': '195.239.187.14:8080'},
    'Санкт-Петербург': {'HTTPS': '94.140.208.226:8080'},
    'Краснодар': {'HTTP': '46.35.249.189:56677'},
    'Томск': {'HTTP': '178.176.240.49:8080'},
    'Тюмень': {'HTTP': '89.250.152.76:8080'},
    'Махачкала': {'SOCKS5': '77.232.160.117:9999'},
    'Калининград': {'SOCKS4': '31.192.155.74:4145'},
    'Рязань': {'SOCKS4': '109.94.182.9:4145'},
    'Владимир': {'SOCKS4': '109.201.96.222:4145'},
    'Курск': {'SOCKS4': '77.241.20.215:31056'},
    'Тамбов': {'SOCKS4': '37.235.206.211:4145'},
    'Новосибирск': {'HTTPS': '80.89.133.210:3128'},
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

>>>>>>> origin/master

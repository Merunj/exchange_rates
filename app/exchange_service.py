import aiohttp
import xml.etree.ElementTree as ET
import redis
import asyncio

url = "https://cbr.ru/scripts/XML_daily.asp"

async def fetch_currency_rates():
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

def parse_currency_rates(xml_data):
    root = ET.fromstring(xml_data)
    rates = {}
    for currency in root.findall('Valute'):
        code = currency.find('CharCode').text
        rate = float(currency.find('Value').text.replace(',', '.')) / float(currency.find('Nominal').text)
        rates[code] = rate
    return rates

def save_rates_to_redis(rates):
    r = redis.Redis(host='127.0.0.1', port='6379')
    for code, rate in rates.items():
        r.set(code, rate)


async def update_exchange_rates():
    xml_data = await fetch_currency_rates()
    rates = parse_currency_rates(xml_data)
    save_rates_to_redis(rates)
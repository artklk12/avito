from bs4 import BeautifulSoup
import time
import asyncio
import aiohttp
import json

start_time = time.time()

all_links = []
all_cards_json = []

async def get_data(session, page):

    url = f"https://www.avito.ru/sankt-peterburg/tovary_dlya_kompyutera/komplektuyuschie/videokarty-ASgBAgICAkTGB~pm7gmmZw?cd=1&p={page}&q=rtx+3050"
    headers = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
    }

    async with session.get(url=url, headers=headers) as response:
        src = await response.text()
        soup = BeautifulSoup(src, "lxml")
        all_cards = soup.find("div", class_="items-items-kAJAg").find_all("div", class_="iva-item-root-_lk9K")

        tasks = []
        for card in all_cards:
            try:
                card_href = "https://www.avito.ru/" + card.find("a").get("href")
            except:
                card_href = "Нет ссылки"
            try:
                card_title = card.find("h3").text
            except:
                card_title = "Нет названия"
            try:
                price = card.find("div", class_="iva-item-priceStep-uq2CQ").text
            except:
                price = 0
            try:
                desc = card.find("div", class_="iva-item-descriptionStep-C0ty1").text
            except:
                desc = "Нет описания"
            try:
                address = card.find("div", class_="geo-root-zPwRk").get_text()
            except:
                address = "Нет адреса"
            try:
                date = card.find("div", class_="iva-item-dateInfoStep-_acjp").text
            except:
                date = "Нет даты публикации"

            all_cards_json.append(
                {
                    "Название": card_title,
                    "Описание": desc,
                    "Цена": price.replace(" ", " "),
                    "Ссылка": card_href,
                    "Адрес": address.replace(" ", " ").rsplit(",")[0],
                    "Дата": date
                }
            )

        await asyncio.gather(*tasks)

async def gather_data():

    url = "https://www.avito.ru/sankt-peterburg/tovary_dlya_kompyutera/komplektuyuschie/videokarty-ASgBAgICAkTGB~pm7gmmZw?cd=1&q=rtx+3050"
    headers = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
    }
    async with aiohttp.ClientSession() as session:
        r = await session.get(url=url, headers=headers)
        soup = BeautifulSoup(await r.text(), "lxml")
        pages_count = int(soup.find_all("a", class_="pagination-page")[-2].text)

        tasks = []

        for page in range(1, pages_count + 1):
            task = asyncio.create_task(get_data(session, page))
            tasks.append(task)

        await asyncio.gather(*tasks)

def main():
    asyncio.run(gather_data())

    with open(f"all_cards.json", "w", encoding="utf-8") as file:
        json.dump(all_cards_json, file, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    main()
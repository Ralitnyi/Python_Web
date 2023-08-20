import asyncio
import json
from datetime import datetime, timedelta
from sys import argv, exit
from time import time

import aiohttp


class CurrencyScraper:
    def calculate_date_days_ago(self, day):
        ago = timedelta(days=day - 1)
        today = datetime.today()
        result_date = today - ago
        return datetime.strftime(result_date, "%d.%m.%Y")

    async def fetch_currency(self, day, extra_currency):
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(limit=10)
        ) as session:
            async with session.get(
                f"https://api.privatbank.ua/p24api/exchange_rates?date={day}"
            ) as response:
                if response.status == 200:
                    html = await response.text()
                    html = json.loads(html)

                    rates = html.get("exchangeRate")
                    currency_info = {day: {}}
                    for money in rates:
                        if money["currency"] in ["USD", "EUR", *extra_currency]:
                            currency_info[day].update(
                                {
                                    money["currency"]: {
                                        "sale": money["saleRate"],
                                        "purchase": money["purchaseRate"],
                                    }
                                }
                            )
                    return currency_info

    async def scrape_exchange_rates(self, num_of_days, extra_currency):
        days = [
            self.calculate_date_days_ago(date) for date in range(1, num_of_days + 1)
        ]
        tasks = [self.fetch_currency(day, extra_currency) for day in days]
        data = await asyncio.gather(*tasks)

        formatted_data = json.dumps(data, indent=2, ensure_ascii=False)
        print(formatted_data)


if __name__ == "__main__":
    start_time = time()
    num_of_days = int(argv[1])
    extra_currency = argv[2:]

    if num_of_days > 10:
        print("END")
        exit()

    scraper = CurrencyScraper()
    asyncio.run(scraper.scrape_exchange_rates(num_of_days, extra_currency))

    end_time = time()
    elapsed_time = end_time - start_time
    print(f"Total execution time: {elapsed_time:.2f} seconds")

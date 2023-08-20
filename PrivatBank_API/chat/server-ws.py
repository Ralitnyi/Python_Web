import asyncio
import json
import logging
from datetime import datetime, timedelta

import aiofile
import aiohttp
import names
import websockets
from aiopath import AsyncPath
from websockets import WebSocketProtocolError, WebSocketServerProtocol

logging.basicConfig(level=logging.INFO)


def process_string(input_string):
    input_string = input_string.strip().casefold()

    if input_string.startswith("exchange"):
        words = input_string.split()
        command = words[0]
        content = tuple(word for word in words[1:])

        if content and not content[0].isdigit():
            return command, (1, *content)
        return command, content
    return input_string


class CurrencyScraper:
    def calculate_date_days_ago(self, day):
        ago = timedelta(days=day - 1)
        today = datetime.today()
        result_date = today - ago
        return datetime.strftime(result_date, "%d.%m.%Y")

    async def fetch_currency(self, date, extra_currency):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.privatbank.ua/p24api/exchange_rates?date={date}"
            ) as response:
                if response.status == 200:
                    html = await response.text()
                    html = json.loads(html)

                    rates = html.get("exchangeRate")
                    currency_info = {date: {}}

                    for money in rates:
                        if money["currency"] in ["USD", "EUR", *extra_currency]:
                            currency_info[date].update(
                                {
                                    money["currency"]: {
                                        "sale": money["saleRateNB"],
                                        "purchase": money["purchaseRateNB"],
                                    }
                                }
                            )
                    return currency_info

    async def scrape_exchange_rates(self, num_of_days=1, extra_currency=None):
        num_of_days = int(num_of_days)
        if num_of_days > 5:
            return "number of days cannot be more than 5"

        days = [
            self.calculate_date_days_ago(date)
            for date in range(1, int(num_of_days) + 1)
        ]

        if extra_currency:
            extra_currency = [ex.upper() for ex in extra_currency]
            tasks = [self.fetch_currency(day, extra_currency) for day in days]
        else:
            tasks = [self.fetch_currency(day, []) for day in days]

        data = await asyncio.gather(*tasks)

        formatted_data = json.dumps(data, indent=2, ensure_ascii=False)
        return formatted_data


class Server:
    def __init__(self, log_file_path):
        self.log_file_path = log_file_path
        self.clients = set()

    async def log_message(self, message):
        async with aiofile.async_open(self.log_file_path, "a") as f:
            await f.write(f"{datetime.now()} - {message}\n")

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f"{ws.remote_address} connects")

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f"{ws.remote_address} disconnects")

    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distrubute(ws)
        except WebSocketProtocolError as err:
            logging.error(err)
        finally:
            await self.unregister(ws)

    async def distrubute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            command_message = process_string(message)

            if type(command_message) == tuple and command_message[0] == "exchange":
                await self.log_message(message)
                await self.send_to_clients("loading...")

                currency = CurrencyScraper()
                try:
                    # if input = exchange n USD EUR ... ... n= number of days
                    m = await currency.scrape_exchange_rates(
                        command_message[1][0], command_message[1][1:]
                    )
                except IndexError:
                    # if input = exchange
                    m = await currency.scrape_exchange_rates()
                await self.send_to_clients(m)
            else:
                await self.send_to_clients(f"{ws.name}: {message}")


async def main():
    log_file_path = "log_file.txt"
    server = Server(log_file_path)
    async with websockets.serve(server.ws_handler, "localhost", 8080):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())

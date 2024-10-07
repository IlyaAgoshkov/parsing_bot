from aiogram import Bot
from aiogram.fsm.context import FSMContext
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from cachetools import TTLCache
from bot.config.config import LOGIN_URL, PASSWORD, USERNAME
from bot.models.StreamerManager import StreamerManager

manager = StreamerManager()
cache = TTLCache(maxsize=100, ttl=30)

async def get_table_value(channel_name):
    if channel_name in cache:
        return cache[channel_name]

    async with aiohttp.ClientSession() as session:
        login_data = {
            'login': USERNAME,
            'password': PASSWORD,
            'utype': 'manager',
            'auth': '1'
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        async with session.post(LOGIN_URL, data=login_data, headers=headers) as login_response:
            if login_response.status != 200:
                print("Не удалось авторизоваться на сайте")
                return None

        async with session.get('https://greedseed.world/p/?type=active') as response:
            if response.status != 200:
                print(f"Ошибка при запросе страницы: {response.status}")
                return None

            soup = BeautifulSoup(await response.text(), 'html.parser')
            row = soup.find('a', string=lambda text: text and text.strip().lower() == channel_name.lower())

            if row:
                tr = row.find_parent('tr')
                if tr:
                    cells = tr.find_all('td')
                    if len(cells) >= 6:
                        percent = cells[6].find('h6').text.strip()
                        percent_value = percent.replace('%', '').strip()
                        # Сохраняем результат в кэш
                        cache[channel_name] = int(percent_value)
                        return int(percent_value)
    return None


async def monitor_streamers(user_id: int, bot: Bot, state: FSMContext):
    while await state.get_state() == "MonitoringStates:monitoring":
        manager.load_data()
        streamers = manager.get_streamers()
        if not streamers:
            await bot.send_message(user_id, "Нет стримеров для мониторинга.")
            break

        messages = []
        tasks = []

        for channel_name, data in streamers.items():
            tasks.append(get_table_value(channel_name))

        values = await asyncio.gather(*tasks)

        for channel_name, value in zip(streamers.keys(), values):
            if value is not None:
                if manager.min_percent <= value <= manager.max_percent:
                    messages.append(f"{channel_name}: {value}% (в пределах нормы)")
                else:
                    messages.append(f"{channel_name}: {value}% (вне допустимых значений)")
                manager.update_percent(channel_name, value)
            else:
                messages.append(f"{channel_name}: Возможно стример завершил стрим.")

        if messages:
            await bot.send_message(user_id, "\n".join(messages))
        else:
            await bot.send_message(user_id, "Нет данных по стримерам.")

        await asyncio.sleep(5)
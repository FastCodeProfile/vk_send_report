import json
import asyncio
from contextlib import suppress

import aiohttp
from loguru import logger


class VkApi:
    def __init__(self, access_token: str) -> None:
        self.host = 'https://api.vk.com/method/'
        self.params = {'v': 5.131}
        self.headers = {'Authorization': f"Bearer {access_token}"}

    async def send_report(self, user_id: str, report_type: str) -> bool:
        method = 'users.report'
        self.params["type"] = report_type
        self.params["user_id"] = user_id
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(self.host + method, params=self.params) as response:
                json_response = await response.json()
                return 'error' not in json_response


def load_data(filename: str) -> dict:
    with open(filename, encoding='utf-8') as file:
        return json.load(file)


async def main() -> None:
    data = load_data('data.json')
    user_id = input('Введите цифровой id пользователя: ')
    report_type = input('Введите тип жалобы(porn, spam, insult, advertisеment): ')
    for key, user in data.items():
        vk_api = VkApi(user['access_token'])
        result = await vk_api.send_report(user_id, report_type)
        if result:
            logger.success(f'Отправлена жалоба - https://vk.com/id{user_id}')
        else:
            logger.error(f'Возникла проблема - {user["url_profile"]}')
            logger.warning('Используйте скрипт, что бы отсеять невалидные аккаунты. '
                           'Ссылка на скрипт: https://github.com/FastCodeProfile/vk_check_token.git')


if __name__ == '__main__':
    with suppress(KeyboardInterrupt):
        asyncio.run(main())

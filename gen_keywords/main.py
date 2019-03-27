import json

import aiohttp
import re

from aiohttp import web


def generate_keywords(title: str):
    title = re.sub(r"[^\w\s]+", '', title)
    title = re.sub(r"\s+", ' ', title)
    title_parts = title.split(' ')
    res_list = []
    # print(title_parts)
    for i in range(len(title_parts), 0, -1):
        for j in range(len(title_parts)):
            if j + i > len(title_parts):
                break
            value_array = title_parts[j:i + j]
            value = " ".join(value_array)
            res_list.append(value)
            # print(f"i - {i}, j - {j}: {value}")
    return res_list


async def get_keywords(url: str):
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        match = re.search('<title>(.*?)</title>', await response.text())
        title = match.group(1) if match else None
        if title is None:
            return []
        return generate_keywords(title)


async def handle(request):
    body = await request.json()
    url = body['url']
    keywords = await get_keywords(url)
    return web.Response(text=json.dumps(keywords))


if __name__ == '__main__':
    app = web.Application()
    app.router.add_post('/', handle)
    print('Initialized Gen Keywords Service')
    web.run_app(app, port=9002)

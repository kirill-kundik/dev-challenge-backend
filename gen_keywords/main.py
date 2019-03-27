import asyncio

import aiohttp
import re


async def generate_keywords(title: str):
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


async def get_title(url: str):
    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        match = re.search('<title>(.*?)</title>', await response.text())
        title = match.group(1) if match else 'No title'
        return await generate_keywords(title)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_title('https://google.com'))

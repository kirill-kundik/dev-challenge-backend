import aiohttp


async def check_auth(request):
    # if request.version != aiohttp.HttpVersion11:
    #     return

    peername = request.transport.get_extra_info('peername')
    if peername is not None:
        host, port = peername
        print(host, port)

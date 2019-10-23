import asyncio
from aiohttp import ClientSession

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()
        
async def main():
    async with ClientSession() as session:
        html = await fetch(session,'127.0.0.1:8888')
        print(html)

if __name__ =='__main__':
    asyncio.run(main())
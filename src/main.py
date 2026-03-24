import asyncio
import aiohttp
from typing import Dict, List
from bs4 import BeautifulSoup

async def fetch_metadata(url: str) -> Dict[str, str]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            
            metadata = {
                'title': soup.title.string,
                'description': soup.find('meta', {'name': 'description'})['content'],
                'keywords': ', '.join([tag.string for tag in soup.find_all('meta', {'name': 'keywords'})]),
                'author': soup.find('meta', {'name': 'author'})['content']
            }
            
            return metadata

async def scrape_urls(urls: List[str]) -> List[Dict[str, str]]:
    tasks = [fetch_metadata(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results

async def main():
    urls = [
        'https://example.com',
        'https://another-example.com',
        'https://third-example.org'
    ]
    
    metadata = await scrape_urls(urls)
    
    for item in metadata:
        print(item)

if __name__ == '__main__':
    asyncio.run(main())
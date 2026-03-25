import asyncio
import aiohttp
import json
import ipfsapi

class MetadataScraper:
    def __init__(self, ipfs_nodes):
        self.ipfs_nodes = ipfs_nodes
        self.session = aiohttp.ClientSession()

    async def fetch_metadata(self, url):
        async with self.session.get(url) as response:
            data = await response.json()
            return data

    async def upload_to_ipfs(self, data):
        for node in self.ipfs_nodes:
            try:
                ipfs = ipfsapi.connect(node['host'], node['port'])
                cid = ipfs.add_json(data)
                return cid
            except Exception as e:
                print(f"Error uploading to IPFS node {node['host']}:{node['port']}: {e}")
        raise Exception("Failed to upload to any IPFS node")

    async def scrape_and_upload(self, urls):
        tasks = [self.fetch_metadata(url) for url in urls]
        metadata = await asyncio.gather(*tasks)
        upload_tasks = [self.upload_to_ipfs(data) for data in metadata]
        cids = await asyncio.gather(*upload_tasks)
        return cids

async def main():
    ipfs_nodes = [
        {'host': '127.0.0.1', 'port': 5001},
        {'host': '192.168.1.100', 'port': 5001},
        {'host': '10.0.0.50', 'port': 5001}
    ]
    scraper = MetadataScraper(ipfs_nodes)
    urls = ['https://example.com/metadata', 'https://another.com/data', 'https://third.net/info']
    cids = await scraper.scrape_and_upload(urls)
    print(cids)

if __name__ == '__main__':
    asyncio.run(main())
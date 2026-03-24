import os
import sys
import asyncio
import random
from typing import List, Dict

from .agent import ScraperAgent
from .coordinator import SwarmCoordinator
from .metadata import MetadataExtractor

async def main():
    # Initialize the swarm coordinator
    coordinator = SwarmCoordinator()
    
    # Spawn a set of scraper agents
    agents: List[ScraperAgent] = [
        ScraperAgent(coordinator, MetadataExtractor())
        for _ in range(100)
    ]
    
    # Start the swarm
    await asyncio.gather(*[agent.start() for agent in agents])
    
    # Monitor the swarm and adjust as needed
    while True:
        await asyncio.sleep(60)  # Check every minute
        coordinator.balance_load(agents)
        
if __name__ == "__main__":
    asyncio.run(main())
import asyncio
from scraper import Scraper
from driver_factory import DriverFactory
import time

async def main():
    playwright, browser, context = await DriverFactory.create_browser_context()
    try:
        scraper = Scraper(context)
        await scraper.run()
    finally:
        await browser.close()
        await playwright.stop()

if __name__ == "__main__":
    time_start = time.time()
    asyncio.run(main())
    time_end = time.time()
    print(f"Execution time: {time_end - time_start:.2f} seconds")

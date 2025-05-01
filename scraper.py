from product_scraper import ProductScraper
from config import DEALS_PAGE_URL, CONCURRENCY
from saver import save_to_json
import asyncio

class Scraper:
    def __init__(self, context):
        self.context = context

    async def get_product_urls(self, page):
        await page.goto(DEALS_PAGE_URL)
        await page.wait_for_selector("div.country-selection", state="attached")
        await page.click("a.us-link[href*='intl=nosplash']")
        await page.wait_for_timeout(5000)

        hrefs = await page.locator("h4.sku-title a").evaluate_all("elements => elements.map(el => el.getAttribute('href'))")
        urls = [f"https://www.bestbuy.com{h}" for h in hrefs if h]
        return urls

    async def run(self):
        page = await self.context.new_page()
        urls = await self.get_product_urls(page)
        await page.close()

        sem = asyncio.Semaphore(CONCURRENCY)
        tasks = [
            asyncio.create_task(ProductScraper(self.context, url, sem, idx + 1, len(urls)).scrape())
            for idx, url in enumerate(urls)
        ]

        results = await asyncio.gather(*tasks)
        save_to_json(results)  # Save to JSON
        return results  # Optionally return results for further use

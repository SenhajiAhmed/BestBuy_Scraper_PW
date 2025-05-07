from product_scraper import ProductScraper
from config import DEALS_PAGE_URL, CONCURRENCY
from saver import save_to_json
from url_gestion import BestBuyPaginationURLGenerator
import asyncio
import time

class Scraper:
    def __init__(self, context):
        self.context = context

    async def get_product_urls(self, page):
        generator = BestBuyPaginationURLGenerator(DEALS_PAGE_URL)
        paginated_links = generator.generate_paginated_urls(start=1, end=10)

        all_urls, i = [], 0

        for link in paginated_links:
            await page.goto(link)

            if i == 0:
                i += 1
                await page.wait_for_selector("div.country-selection", timeout=10000)
                
                await page.click("a.us-link[href*='intl=nosplash']")
                await page.wait_for_timeout(5000)

            time.sleep(0.5)

            await page.wait_for_selector("h4.sku-title a", timeout=10000)
            hrefs = await page.locator("h4.sku-title a").evaluate_all(
                "elements => elements.map(el => el.getAttribute('href'))"
            )
            urls = [f"https://www.bestbuy.com{h}" for h in hrefs if h]
            all_urls.extend(urls)

        return all_urls

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
        save_to_json(results)
        return results

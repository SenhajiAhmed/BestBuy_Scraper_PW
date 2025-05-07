from playwright.async_api import TimeoutError

class ProductScraper:
    def __init__(self, context, url, sem, index, total):
        self.context = context
        self.url = url
        self.sem = sem
        self.index = index
        self.total = total

    async def scrape(self):
        async with self.sem:
            page = await self.context.new_page()
            await page.goto(self.url)
            print(f"📦 [{self.index}/{self.total}] Loaded {self.url}")

            try:
                specs_btn = await page.wait_for_selector("div.mb-600 >> button.show-full-specs-btn", timeout=10000)
                if specs_btn:
                    await specs_btn.scroll_into_view_if_needed(timeout=5000)
                    await specs_btn.click(timeout=5000)
                    print(f"🛠 [{self.index}/{self.total}] Clicked default specs button")
                else:
                    raise TimeoutError()

            except TimeoutError:
                try:
                    specs_btn_2 = await page.wait_for_selector("div.v-border-bottom >> button[data-testid='brix-button']", timeout=10000)
                    await specs_btn_2.scroll_into_view_if_needed(timeout=5000)
                    await specs_btn_2.click(timeout=5000)
                    print(f"🛠 [{self.index}/{self.total}] Clicked alternative specs button")
                except TimeoutError:
                    print(f"⚠️  [{self.index}/{self.total}] No specs button found")
            
            await page.wait_for_timeout(2000)
            headers = page.locator("h4.v-text-md.mb-150")
            header_count = await headers.count()

            product_data = {
                "url": self.url,
                "sections": []
            }
            if header_count == 0:
                print(f"ℹ️  [{self.index}/{self.total}] No spec sections")
            else:
                for h in range(header_count):
                    header = headers.nth(h)
                    title = (await header.inner_text()).strip()
                    print(f"\nSection {h+1}: {title}")
                    container = header.locator("xpath=..")
                    keys = container.locator("div.grow.basis-none.font-weight-medium")
                    vals = container.locator("div.grow.basis-none.pl-300")
                    count = await keys.count()

                    section_details = {}
                    for i in range(count):
                        k = (await keys.nth(i).inner_text()).strip()
                        v = (await vals.nth(i).inner_text()).strip()
                        print(f"  • {k}: {v}")
                        section_details[k] = v

                    product_data["sections"].append({
                        "section": title,
                        "details": section_details
                    })

            await page.close()
            print(f"✅ [{self.index}/{self.total}] Done {self.url}")
            return product_data
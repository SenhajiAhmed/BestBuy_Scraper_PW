from playwright.async_api import async_playwright
from config import HEADLESS

class DriverFactory:
    @staticmethod
    async def create_browser_context():
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=HEADLESS)

        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720},
            java_script_enabled=True,
        )

        # Block images, stylesheets, fonts to speed up load
        context.set_default_timeout(300000)  # 30s timeout
        await context.route("**/*", lambda route, request: (
            route.abort() if request.resource_type in ["image", "stylesheet", "font"] else route.continue_()
        ))

        return playwright, browser, context

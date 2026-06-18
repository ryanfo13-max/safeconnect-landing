import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1280, "height": 900})
        await page.goto("http://localhost:3456", wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(2000)

        sections = [
            ("hero", 0),
            ("trust_why", 700),
            ("photo_faq", 1500),
            ("poor_planning", 2400),
            ("why_sc_form", 3300),
            ("footer", 4600),
        ]

        for name, scroll_y in sections:
            await page.evaluate(f"window.scrollTo(0, {scroll_y})")
            await page.wait_for_timeout(300)
            await page.screenshot(
                path=rf"C:\Users\RyanFoss\Downloads\review_{name}.png",
                full_page=False
            )
            print(f"Saved review_{name}.png")

        await browser.close()

asyncio.run(run())

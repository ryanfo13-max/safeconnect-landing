import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1280, "height": 900})
        await page.goto("http://localhost:3456", wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(2000)

        for name, y in [("why_section", 600), ("faq_section", 1100), ("poor_planning", 1700), ("why_sc", 2200)]:
            await page.evaluate(f"window.scrollTo(0, {y})")
            await page.wait_for_timeout(300)
            await page.screenshot(path=rf"C:\Users\RyanFoss\Downloads\sect_{name}.png", full_page=False)
            print(f"Saved sect_{name}.png")

        await browser.close()

asyncio.run(run())

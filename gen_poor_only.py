import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1280, "height": 900})
        await page.goto("http://localhost:3456", wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(2000)
        for name, y in [("poor_top", 1850), ("poor_mid", 2050)]:
            await page.evaluate(f"window.scrollTo(0, {y})")
            await page.wait_for_timeout(300)
            await page.screenshot(path=rf"C:\Users\RyanFoss\Downloads\{name}.png", full_page=False)
            print(f"Saved {name}.png")
        await browser.close()

asyncio.run(run())

import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1280, "height": 900})
        await page.goto("http://localhost:3456", wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(2000)
        await page.screenshot(
            path=r"C:\Users\RyanFoss\Downloads\review_fullpage.png",
            full_page=True
        )
        print("Saved review_fullpage.png")
        await browser.close()

asyncio.run(run())

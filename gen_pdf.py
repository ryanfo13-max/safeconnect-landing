import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1280, "height": 900})
        await page.goto("http://localhost:3456", wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(2000)
        await page.pdf(
            path=r"C:\Users\RyanFoss\Downloads\safeconnect-landing-review.pdf",
            format="A4",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"}
        )
        print("PDF saved to Downloads/safeconnect-landing-review.pdf")
        await browser.close()

asyncio.run(run())

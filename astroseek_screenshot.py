from playwright.sync_api import sync_playwright
import sys
import time

def generate_astroseek_chart(date, time_str, lat, lon, location, output_file):
    day, month, year = date.split("/")
    hour, minute = time_str.split(":")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        context = browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        page = context.new_page()

        page.goto("https://horoscopes.astro-seek.com/astro-chart-horoscope-online/", timeout=60000)
        page.wait_for_selector("input[name='nick']", timeout=10000)

        page.fill("input[name='nick']", "Test User")
        page.select_option("#d", day)
        page.select_option("#m", month)
        page.select_option("#y", year)
        page.select_option("#h", hour)
        page.select_option("#min", minute)

        page.click("text=Enter your exact birth place")
        page.fill("input[name='geo_place_input']", location)
        page.wait_for_timeout(3000)
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")

        page.click("input[type='submit'][value='Continue »']")
        page.wait_for_load_state("networkidle")
        page.wait_for_selector("img.chart_img", timeout=15000)

        chart_img = page.query_selector("img.chart_img")
        chart_img.screenshot(path=output_file)

        browser.close()

if __name__ == "__main__":
    _, date, time_str, lat, lon, location, output_file = sys.argv
    generate_astroseek_chart(date, time_str, lat, lon, location, output_file)

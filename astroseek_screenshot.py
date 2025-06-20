from playwright.sync_api import sync_playwright
import sys
import time

def generate_astroseek_chart(date, time_str, lat, lon, location, output_file):
    # Data parsing
    day, month, year = date.split("/")
    hour, minute = time_str.split(":")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        page.goto("https://horoscopes.astro-seek.com/astro-chart-horoscope-online/")

        # Compila nome fittizio
        page.wait_for_selector("#nick", timeout=10000)
        page.fill("#nick", "Test User")

        # Inserisci data e ora
        page.select_option("#d", day)
        page.select_option("#m", month)
        page.select_option("#y", year)
        page.select_option("#h", hour)
        page.select_option("#min", minute)

        # Luogo di nascita (custom)
        page.click("text=Enter your exact birth place")
        page.fill("input[name='geo_place_input']", location)
        page.wait_for_timeout(2000)  # attesa suggerimenti
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")

        # Attendi che la carta venga generata
        page.click("input[type='submit']")
        page.wait_for_load_state("networkidle")
        page.wait_for_selector("img.chart_img")

        # Screenshot solo della carta
        chart_img = page.query_selector("img.chart_img")
        chart_img.screenshot(path=output_file)

        browser.close()

if __name__ == "__main__":
    # Esempio: python3 astroseek_screenshot.py 15/08/1990 14:30 41.9028 12.4964 "Rome, Italy" chart.png
    _, date, time_str, lat, lon, location, output_file = sys.argv
    generate_astroseek_chart(date, time_str, lat, lon, location, output_file)

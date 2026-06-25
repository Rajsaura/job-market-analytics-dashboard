import os

from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options

SCRAPEOPS_API_KEY = os.environ["SCRAPEOPS_API_KEY"]

proxy_options = {
    "proxy": {
        "http": f"http://scrapeops.headless_browser_mode=true:{SCRAPEOPS_API_KEY}@proxy.scrapeops.io:5353",
        "https": f"http://scrapeops.headless_browser_mode=true:{SCRAPEOPS_API_KEY}@proxy.scrapeops.io:5353",
        "no_proxy": "localhost,127.0.0.1"
    }
}

options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(
    seleniumwire_options=proxy_options,
    options=options
)

driver.get("https://api.ipify.org")

print(driver.page_source)

driver.get("https://www.naukri.com/data-scientist-jobs")

driver.save_screenshot("test.png")

with open("test.html","w",encoding="utf-8") as f:
    f.write(driver.page_source)

driver.quit()
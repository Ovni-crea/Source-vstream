from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options



def bypass_cloudflare(url):
    path = "C:/Users/USERNAME/AppData/Roaming/Kodi/addons/script.module.selenium/bin/geckodriver/win32/geckodriver/geckodriver.exe"
    options.headless = False
    browser = webdriver.Firefox(executable_path=path, options=options, log_path="C:/Users/USERNAME/geckodriver.log")
    browser.get(url)
    time.sleep(10)
    page_source = (driver.page_source).encode('utf-8', errors='replace')
    driver.close()
    print(page_source)
    sHtmlContent = page_source
    return sHtmlContent
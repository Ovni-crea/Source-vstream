def bypass_cloudflare_linux(url):
    driverPath = get_driver_path('chromedriver')
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=/home/USERNAME/chrome")
    driver = webdriver.Chrome(driverPath, chrome_options=options)
    options.headless = False
    driver.get(url)
    time.sleep(10)
    page_source = (driver.page_source).encode('utf-8', errors='replace')
    driver.close()
    print(page_source)
    sHtmlContent = page_source
    return sHtmlContent

def bypass_cloudflare(url):
    driverPath = get_driver_path('chromedriver')
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=C:\cookie")
    driver = webdriver.Chrome(driverPath, chrome_options=options)
    options.headless = False
    driver.get(url)
    time.sleep(10)
    page_source = driver.page_source
    driver.close()
    print(page_source)
    sHtmlContent = page_source
    return sHtmlContent

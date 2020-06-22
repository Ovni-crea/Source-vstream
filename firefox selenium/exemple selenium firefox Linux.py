from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import os 



def bypass_cloudflare(url):
	os.chmod('/home/USERNAME/.kodi/addons/script.module.selenium/bin/geckodriver/linux64/geckodriver/geckodriver', 0755)
    	path = "/home/USERNAME/.kodi/addons/script.module.selenium/bin/geckodriver/linux64/geckodriver/geckodriver"
    	options.headless = False
    	browser = webdriver.Firefox(executable_path=path, options=options, log_path="/home/USERNAME/geckodriver.log")
    	browser.get(url)
    	time.sleep(10)
    	page_source = (driver.page_source).encode('utf-8', errors='replace')
    	driver.close()
    	print(page_source)
    	sHtmlContent = page_source
    	return sHtmlContent

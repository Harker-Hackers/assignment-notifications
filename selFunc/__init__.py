from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import re

cPath=os.environ.get("CHROMEPATH")

def getCourses(a,b):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    driver.get("https://schoology.harker.org/courses")
    user = driver.find_element_by_name("mail")
    passw=driver.find_element_by_name("pass")
    user.clear()
    user.send_keys(a)
    passw.send_keys(b)
    passw.send_keys(Keys.RETURN)
    data=driver.page_source
    result = re.findall("id=\"course-(.*?)\"",data)
    print(result)
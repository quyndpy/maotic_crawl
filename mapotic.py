from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import json
class Mapotic_Bot():
    def __init__(self):
        self.driver = webdriver.Chrome()
    def load_mapotic(self):
        self.driver.get('https://www.mapotic.com/samoobsluzne-myci-boxy/places?zoom=2&lng=42.32492885688873&lat=42.919686388639235')

        try: 
            while True:
                time.sleep(3)
                load_more_button = self.driver.find_element(By.CLASS_NAME, 'btn-normal')
                if load_more_button.is_displayed():
                    load_more_button.click()
                else:
                    break
        except NoSuchElementException:
            print("Nút không còn hiển thị")
    def scrapy_url(self):
        time.sleep(3)
        extracted_product_names = []
        # self.driver.find_elements(By.XPATH, "//a[starts-with(@href, '/samoobsluzne-myci-boxy/')]")
        link_elements = self.driver.find_elements(By.CSS_SELECTOR,'a[custom-list-item]')
        for element in link_elements:
            url = element.get_attribute('href')
            extracted_product_names.append(url)
        return extracted_product_names
    def run(self):
        self.load_mapotic()
        extracted_product_names =  self.scrapy_url()
        data = {"url": extracted_product_names}
        json_file_path = "url_map.json"
        with open(json_file_path,"w") as json_file:
            json.dump(data,json_file, indent=4)
# python -i mapotic.py
bot = Mapotic_Bot()
bot.run()


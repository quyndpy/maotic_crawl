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
    def scrapy_mapotic(self, url):
        self.driver.get(url)
        time.sleep(6)
        title = self.driver.find_element(By.CLASS_NAME, 'title').text
        subtitle = self.driver.find_element(By.CLASS_NAME,'subtitle').text
        user_name = self.driver.find_element(By.CLASS_NAME,'user-avatar-name').text
        data = {
            "title": title,
            "subtitle": subtitle,
            "user_name": user_name,
            "attributes": []
        }
        cha_elements = self.driver.find_elements(By.CSS_SELECTOR, 'attributes-view-switch')
        for cha_element in cha_elements:
            con_element1 = cha_element.find_element(By.CLASS_NAME, 'icon-wrap')
            mat_icon_type = con_element1.find_element(By.TAG_NAME,'mat-icon').get_attribute('data-mat-icon-name')

            con_element2 = cha_element.find_element(By.CLASS_NAME, 'mat-tooltip-trigger.wrap-body')
            text_from_element2 = con_element2.text

            data["attributes"].append({
                "mat_icon_type": mat_icon_type,
                "text_from_element2": text_from_element2
            })
        cha2 = self.driver.find_element(By.CSS_SELECTOR, 'attributes-view-location-gps')
        GPSs = cha2.find_element(By.CLASS_NAME, 'mat-tooltip-trigger.wrap-body').text
        GPS_address = self.driver.find_element(By.CSS_SELECTOR, 'w3w-link').text

        # Thêm dữ liệu GPS vào từ điển
        data["GPS"] = GPSs
        data["GPS_address"] = GPS_address

        # Lấy URL hình ảnh
        url_photo = self.driver.find_element(By.CLASS_NAME, 'image-thumb').get_attribute('src')

        # Thêm URL hình ảnh vào từ điển
        data["url_photo"] = url_photo

        return data
    def scrapy_mapotic_url(self, urls):
        all_data = []
        for url in urls:
            # Gọi scrapy_mapotic và thêm dữ liệu cho URL hiện tại vào danh sách tất cả dữ liệu
            data_for_url = self.scrapy_mapotic(url)
            all_data.append(data_for_url)
        
        # Ghi tất cả dữ liệu vào tệp JSON
        with open('data.json', 'w', encoding='utf-8') as json_file:
            json.dump(all_data, json_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    with open('your_file.json', 'r') as json_file:  # Đọc tệp JSON
        data = json.load(json_file)
        urls = data["url"]  # Lấy danh sách URL từ tệp JSON
    bot = Mapotic_Bot()
    bot.scrapy_mapotic_url(urls)  # Gọi hàm để scrap và lưu nhiều URL

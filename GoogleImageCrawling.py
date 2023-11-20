from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from urllib.request import urlretrieve
import time
import os


chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

url = "https://www.google.co.kr/imghp"


class OpenPage:

    def __init__(self):
        self.driver = driver.get(url=url)
        self.count = 0

    
    def searching_image(self):
        self.keyword = input("검색항목 : ")
        if self.count == 0:
            self.search = driver.find_element(By.CLASS_NAME, "gLFyf")
            self.count += 1
        else:
            self.search = driver.find_element(By.CLASS_NAME, "og3lId")

        self.search.clear()
        self.search.send_keys(self.keyword)
        self.search.send_keys(Keys.RETURN)


    def find_image(self):
        images = driver.find_elements(By.CLASS_NAME, "rg_i.Q4LuWd")
        limit = input(f"{len(images)}개 중 이미지 개수 : ")

        try:
            limit = int(limit)

            if len(images) >= limit and len(images) > 0:
                crawling_images(self.keyword, images, limit)

            else:
                images = scrollDown(images, limit)
                crawling_images(self.keyword, images, limit)

        except:
            if limit == '재검색':
                self.searching_image()
            
            print("정수로 입력해주세요.")
            self.find_image()
            

    def closePage(self):
        driver.close()


def scrollDown(images, limit):
    while limit > len(images):
        action = ActionChains(driver)
        action.move_to_element(images[-1]).perform()

        images = driver.find_elements(By.CLASS_NAME, "rg_i.Q4LuWd")
        print(f"이미지 {len(images)}개 찾음")

    return images


def crawling_images(keyword, images, limit):
    current_path = "./data"
    folder = keyword
    image_folder = os.path.join(current_path, folder)
    name = input("저장할 이름을 적어주세요 : ")
    wrong = []

    if not os.path.isdir(image_folder):
        os.makedirs(image_folder)

    for idx, image in enumerate(images[:limit]):
            try:
                src = image.get_attribute("src")
                filename = f"{name}{str(idx)}.jpg"
                filepath = os.path.join(image_folder, filename)
                urlretrieve(src, filepath)
            except:
                print(f'{idx}번째 이미지 오류')
                wrong.append(image)

    print(f"{limit - len(wrong)}장 저장되었습니다.")


def main():
    a = OpenPage()
    

    while True:
        a.searching_image()
        time.sleep(0.5)
        a.find_image()

        stop_word = input("Stop? : ")
        
        if stop_word == "1":
            break

    a.closePage()


if __name__ == "__main__":
    main()
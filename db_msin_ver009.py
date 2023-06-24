# ver0.0.9

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# 提示使用者輸入搜尋名稱
search_name = input("請輸入要搜尋的名稱：")

# 設定 WebDriver 使用 headless 模式（背景執行）
options = Options()
options.add_argument("--headless")

# 開啟瀏覽器並訪問網站
driver = webdriver.Chrome(options=options)  # 或是你正在使用的其他瀏覽器
driver.get("https://db.msin.jp/?jp")


try:
    # 點擊 Enter 元素
    click_xpath = "/html/body/div[7]/div[2]/img[1]"
    element_to_click = driver.find_element(By.XPATH, click_xpath)
    element_to_click.click()

    # 填入搜尋欄位
    search_xpath = "//*[@id='head_search_ber']/div/form/input"
    search_input = driver.find_element(By.XPATH, search_xpath)
    search_input.clear()
    search_input.send_keys(search_name)

    # 提交表單進行搜尋
    search_input.send_keys(Keys.RETURN)

    # 等待頁面載入
    driver.implicitly_wait(5)

    # 定義要爬取的元素 XPath
    xpath_dict = {
        "Headshot": "//*[@id='top_content']/div[2]/div[1]/div[1]/a",
        "Name": "//*[@id='top_content']/div[2]/div[2]/div[1]",
        "Alias": "//*[@id='top_content']/div[2]/div[2]/span[2]",
        "Birthday": "//*[@id='top_content']/div[2]/div[2]/span[1]",
        "Height": "//*[@id='top_content']/div[2]/div[2]/span[3]/span[1]",
        "Bust": "//*[@id='top_content']/div[2]/div[2]/span[3]/span[2]",
        "Cup": "//*[@id='top_content']/div[2]/div[2]/span[3]/span[3]",
        "Waistline": "//*[@id='top_content']/div[2]/div[2]/span[3]/span[4]",
        "Hip": "//*[@id='top_content']/div[2]/div[2]/span[3]/span[5]",
        "BloodType": "//*[@id='top_content']/div[2]/div[2]/span[4]",
        "Twitter": "//*[@id='top_content']/div[2]/div[2]/div[8]/div[2]/a",
        "Instagram": "//*[@id='top_content']/div[2]/div[2]/div[8]/div[5]/a",
    }

    # 爬取對應資料
    data = {}
    for key, xpath in xpath_dict.items():
        try:
            element = driver.find_element(By.XPATH, xpath)
            if key == "Headshot":
                data[key] = element.get_attribute("href")
            else:
                data[key] = element.text
        except:
            data[key] = ""

    # 將資料轉換成圖片網址
    if data["Headshot"]:
        image_id = data["Headshot"].split("id=")[1]
        data["Headshot"] = "https://img.msin.info/jp.images/actress/{}.jpg".format(image_id)

    # 定義要爬取的元素 CSS 選擇器
    css_selector_dict = {
        "Interest": "#top_content > div.actress_info_ditail > div.act_ditail > span.mv_hobby",
        "Birthplace": "#top_content > div.actress_info_ditail > div.act_ditail > span.mv_birthplace",
        "LoginPeriod": "#top_content > div.actress_info_ditail > div.act_ditail > span:nth-child(17)",
    }

    # 爬取css對應資料
    for key, css_selector in css_selector_dict.items():
        try:
            element = driver.find_element(By.CSS_SELECTOR, css_selector)
            data[key] = element.text
        except:
            data[key] = ""

    # 輸出資料
    print("大頭照:", data["Headshot"])
    print("名稱:", data["Name"])
    print("別名:", data["Alias"])
    print("生日:", data["Birthday"])
    print("身高:", data["Height"])
    print("胸圍:", data["Bust"])
    print("罩杯:", data["Cup"])
    print("腰圍:", data["Waistline"])
    print("臀圍:", data["Hip"])
    print("血型:", data["BloodType"])
    print("興趣:", data["Interest"])
    print("出生地:", data["Birthplace"])
    print("登入期間（件數）:", data["LoginPeriod"])
    print("Twitter:", data["Twitter"])
    print("Instagram:", data["Instagram"])

except Exception as e:
    print("發生錯誤：", str(e))

finally:
    # 關閉瀏覽器
    driver.quit()

import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select

# webdriver
from selenium import webdriver


from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from undetected_chromedriver import Chrome, ChromeOptions
import pyautogui
import os
from selenium.webdriver.support.ui import Select


# ############
s1 = "UTBurlington"
s2 = "76"

img_directory = "C://Users/Phoebus/Desktop/DIP_Project/images/original/UTBurlington/"

new_path1 = "C://Users/Phoebus/Desktop/DIP_Project/Landmarks_CSV/UTBurlington/"
######################################################################
WebAddr1 = "https://www.aaoflegacycollection.org/aaof_LMTableDisplay.html?collectionID="
WebAddr2 = "&subjectID="

NO_HEAD = 0
WAIT_SEC = 15


directory = img_directory
list_sers = []
for filename in os.listdir(directory):

    if filename.endswith(".png"):
        result = filename.split("_")
        list_sers.append(result[1])


unique_list_sers = list(set(list_sers))
print("numbers：")
print(len(unique_list_sers))
print("series：")
print(unique_list_sers)


def download_CSV(s2):

    try:
        element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div/div/div/ul/li[2]/a")
            )
        )
    except:
        print("end...")
        time.sleep(200)
        driver.quit()

    above = driver.find_element(By.XPATH, "/html/body/div/div/div/ul/li[2]/a")

    ActionChains(driver).click(above).perform()

    try:
        element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, "//html/body/div/div/div/div[2]/div/div[1]/a[2]/span")
            )
        )
    except:
        print("end...")
        time.sleep(200)
        driver.quit()

    above = driver.find_element(
        By.XPATH, "//html/body/div/div/div/div[2]/div/div[1]/a[2]/span"
    )

    ActionChains(driver).click(above).perform()

    time.sleep(2)

    new_path = new_path1
    new_filename = s1 + "_" + s2 + "_Tables.csv"
    new_filename_path = new_path + new_filename
    os.rename(
        "C://Users/Phoebus/Downloads/Display AAOF Landmark Tables.csv",
        new_filename_path,
    )
    print("complete：" + new_filename)
    time.sleep(2)


# undetected_chromedriver
from webdriver_manager.chrome import ChromeDriverManager

latestchromedriver = ChromeDriverManager().install()

service = Service()
options = ChromeOptions()
# options.add_argument(
#     "--headless"
# driver = Chrome(service=service, options=options)
# undetected_chromedriver
driver = Chrome(driver_executable_path=latestchromedriver, options=options)


for index, sers_name in enumerate(unique_list_sers):
    WebAddr = WebAddr1 + s1 + WebAddr2 + sers_name
    driver.get(WebAddr)
    print("-----now dealing：" + str(index + 1) + "/" + str(len(unique_list_sers)))
    download_CSV(sers_name)


print("end...")
time.sleep(200)
driver.quit()

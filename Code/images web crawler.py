import time
import sys
import numpy as np
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select

# webdriver
from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
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


download_path = "C://Users/Phoebus/Desktop/DIP_Project/images/original/UTBurlington/"
collection = "UTBurlington"
flag = 1
sers_over = "006"
sers_index = 0
passsssnum = 27
flag_passsssnum = 0
##############################################
WebAddr1 = "https://www.aaoflegacycollection.org/aaof_multiview.html?collectionID="
s1 = collection
WebAddr2 = "&subjectID="
s2 = "76"
WebAddr3 = "&imageType="
s3 = "1"
WebAddr4 = "&imageNumber="
s4 = "1"

NO_HEAD = 0
WAIT_SEC = 15

fail_order = []


def download_key():

    time.sleep(0.5)
    pyautogui.typewrite(["v"], 0.5)

    pyautogui.typewrite(["enter"], 0.5)

    # time.sleep(0.5)


def load_2images():

    if os.path.exists("C://Users/Phoebus/Downloads/下载.png"):
        print("removed....")
        os.remove("C://Users/Phoebus/Downloads/下载.png")
        time.sleep(0.5)

    above = driver.find_element(
        By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[3]/canvas"
    )

    ActionChains(driver).context_click(above).perform()

    WebDriverWait(driver, 15, 5).until(EC.alert_is_present())
    driver.switch_to.alert.accept()

    download_key()

    new_path = download_path
    new_filename = s1 + "_" + s2 + "_" + s3 + "_" + s4 + "_NoLabel.png"
    new_filename_path = new_path + new_filename

    duration = 15

    start_time = time.time()

    while (time.time() - start_time) < duration:
        if os.path.exists("C://Users/Phoebus/Downloads/下载.png"):
            os.rename("C://Users/Phoebus/Downloads/下载.png", new_filename_path)
            print("done：" + new_filename)
            break
        else:
            print("--skip!!!")
            # driver.switch_to.alert.accept()

            nname = s1 + WebAddr2 + s2 + WebAddr3 + s3 + WebAddr4 + s4
            fail_order.append(nname)
            time.sleep(5)

            return

        time.sleep(interval)

    driver.find_element(
        By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[5]/div[2]/input[1]"
    ).click()
    time.sleep(0.1)
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[5]/div[2]/input[2]"
    ).click()
    time.sleep(0.1)
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[5]/div[2]/input[3]"
    ).click()
    time.sleep(0.1)
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[5]/div[2]/input[4]"
    ).click()
    time.sleep(0.1)
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[5]/div[4]/input"
    ).click()

    time.sleep(1)

    above = driver.find_element(
        By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[3]/canvas"
    )

    ActionChains(driver).context_click(above).perform()

    WebDriverWait(driver, 15, 5).until(EC.alert_is_present())
    driver.switch_to.alert.accept()

    download_key()

    new_path = download_path
    new_filename = s1 + "_" + s2 + "_" + s3 + "_" + s4 + "_WithLabel.png"
    new_filename_path = new_path + new_filename

    duration = 15

    interval = 0.5

    start_time = time.time()

    while (time.time() - start_time) < duration:
        if os.path.exists("C://Users/Phoebus/Downloads/下载.png"):
            os.rename("C://Users/Phoebus/Downloads/下载.png", new_filename_path)
            print("done：" + new_filename)
            break
        else:
            print("--skip!!!")
            driver.switch_to.alert.accept()

            nname = s1 + WebAddr2 + s2 + WebAddr3 + s3 + WebAddr4 + s4
            fail_order.append(nname)
            time.sleep(5)

            return

        time.sleep(interval)


# undetected_chromedriver
from webdriver_manager.chrome import ChromeDriverManager

latestchromedriver = ChromeDriverManager().install()

service = Service()
options = ChromeOptions()

driver = Chrome(driver_executable_path=latestchromedriver, options=options)
WebAddr = WebAddr1 + s1 + WebAddr2 + s2 + WebAddr3 + s3 + WebAddr4 + s4
driver.get(WebAddr)

driver.maximize_window()
time.sleep(4)


save_file = collection
save_path = save_file + "_crawler.npz"
if os.path.exists(save_path) == False:
    select = Select(
        driver.find_element(
            By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[4]/div[2]/select"
        )
    )

    options = select.options

    option_texts = [o.get_attribute("textContent") for o in options]

    symbol = "*"
    seris_list_withLable = []
    for text in option_texts:
        if symbol in text:
            seris_list_withLable.append(text[:-1])
    print("lebal seris：")
    print(seris_list_withLable)

    ############
    np.savez(save_path, list=seris_list_withLable, pass_order=sers_index)

else:
    ############
    loaded_arrays = np.load(save_path, allow_pickle=True)

    seris_list_withLable = loaded_arrays["list"]
    sers_index = loaded_arrays["pass_order"]


###########
if flag_passsssnum == 1:
    np.savez(save_path, list=seris_list_withLable, pass_order=passsssnum)


for index, current_ses in enumerate(seris_list_withLable):
    # for current_ses in seris_list_withLable:
    s2 = str(current_ses)

    if (s2 != sers_over) and (flag == 0):
        print("----- skip：" + s2)
        continue
    if s2 == sers_over:
        flag = 1

    if sers_index > index:
        print("----- skip：" + s2)
        continue

    s4 = "1"
    print("-----now seris：" + s2)
    print("-----now dealing：" + str(index) + "/" + str(len(seris_list_withLable)))
    WebAddr = WebAddr1 + s1 + WebAddr2 + s2 + WebAddr3 + s3 + WebAddr4 + s4
    driver.get(WebAddr)

    try:  # case："/html/body/div[1]/div[3]/div[1]/div[4]/div[3]/select"
        element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[5]/div[1]/button[1]")
            )
        )
    except:
        print("skip...")
        time.sleep(5)
        continue

    select = Select(
        driver.find_element(
            By.XPATH, "/html/body/div[1]/div[3]/div[1]/div[4]/div[3]/select"
        )
    )

    options = select.options

    option_texts = [o.get_attribute("textContent") for o in options]

    symbol = "*"
    i = 0
    list_withLable = []
    for text in option_texts:
        i += 1
        if symbol in text:
            list_withLable.append(i)
    print("in" + s2 + "label order：")
    print(list_withLable)

    for current_img in list_withLable:
        s4 = str(current_img)
        print("NO " + s4)

        new_path = download_path
        new_filename = s1 + "_" + s2 + "_" + s3 + "_" + s4 + "_NoLabel.png"
        new_filename_path = new_path + new_filename
        if os.path.exists(new_filename_path):
            print(s4 + "skip....")
            continue

        WebAddr = WebAddr1 + s1 + WebAddr2 + s2 + WebAddr3 + s3 + WebAddr4 + s4
        driver.get(WebAddr)
        time.sleep(0.5)

        try:
            element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        "/html/body/div[1]/div[3]/div[1]/div[5]/div[1]/button[1]",
                    )
                )
            )
        except:
            print("skip...")
            # driver.switch_to.alert.dismiss()
            # driver.switch_to.alert.accept()

            nname = s1 + "_" + s2 + "_" + s3 + "_" + s4
            fail_order.append(nname)
            time.sleep(10)
            continue

        load_2images()

    ############
    np.savez(save_path, list=seris_list_withLable, pass_order=index + 1)
    if fail_order:
        print("failed：")
        print(fail_order)

print("done...")
print("failed：")
print(fail_order)
time.sleep(200)
driver.quit()

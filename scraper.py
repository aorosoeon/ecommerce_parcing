from login_info import optanon_alert_box_closed, optanon_consent, ss_user_id, url
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

service = Service(executable_path="/Users/arsenchuzhykov/Desktop/fastapi/chromedriver") #creating Service object for handling the browser driver
browser = webdriver.Chrome(service=service) #creating a new instance of chromedriver

def get_initial_window():
    browser.get(url)
    sleep(2)
    browser.add_cookie({"name": "ssUserId", "value": ss_user_id})
    browser.add_cookie({"name": "OptanonConsent", "value": optanon_consent})
    browser.add_cookie({"name": "OptanonAlertBoxClosed", "value": optanon_alert_box_closed})
    sleep(2)
    browser.get(url)
    sleep(5)
    WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body"))) #"wait until" to ensure it's loaded

def js_click(browser, button, seconds): #there are different ways of "clicking" something with selenium. when you click something with click() (your see your cursor moves), linkedin can intercept this click and the program will crash. it's linkedin's way of preventing bots. that's why we need to click with javascript - it's a more reliable way of clicking
    WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body"))) #making sure that the page is loaded. if it's not and you will try to click, the program will crash
    browser.execute_script("arguments[0].click();", button) #clicking the element with javascript
    sleep(seconds) #wait to ensure that there is a pause between click and next action

def next_page():
    next_page = browser.find_element(By.XPATH, "//a[@class='action  next' and contains(@ng-href, 'https://www.sail.ca/en/footwear/men?page=')]")
    js_click(browser, next_page, 2) #click send_wo_note button
    sleep(4)
    WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    browser.back()
    sleep(4)

get_initial_window()

page_num = 1

while True:
    browser.get(f"{url}?page={page_num}")
    sleep(5)
    product_links = [link.get_attribute("href") for link in browser.find_elements(By.TAG_NAME, "a") if link.get_attribute("class") == "product-item-link ng-binding"]
    for product_link in product_links:
        browser.get(product_link)
        sleep(5)
    page_num = page_num + 1
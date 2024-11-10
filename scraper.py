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
    sleep(1)
    #browser.add_cookie({"name": "ssUserId", "value": ss_user_id})
    browser.add_cookie({"name": "OptanonConsent", "value": optanon_consent})
    browser.add_cookie({"name": "OptanonAlertBoxClosed", "value": optanon_alert_box_closed})
    sleep(1)
    browser.get(url)
    sleep(5)
    WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body"))) #"wait until" to ensure it's loaded

get_initial_window()
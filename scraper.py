import pandas as pd
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

def js_click(browser, button, seconds):
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

def main():
    get_initial_window()
    names, prices, links, stock_availability = [], [], [], []
    page_num = 1
    while page_num < 4: #limiting to just a couple pages for a demonstration purpose, REMOVE if needed
        browser.get(f"{url}?page={page_num}")
        sleep(5)
        product_links = [link.get_attribute("href") for link in browser.find_elements(By.TAG_NAME, "a") if link.get_attribute("class") == "product-item-link ng-binding"]
        for product_link in product_links[1:3]: #limiting to just a couple items for a demonstration purpose, REMOVE if needed
            browser.get(product_link)
            sleep(5)
            product_name_element = browser.find_element(By.XPATH, "//span[@data-ui-id='page-title-wrapper']")
            names.append(product_name_element.text)
            product_price_element = browser.find_element(By.XPATH, "//span[@class='price']")
            prices.append(product_price_element.text)
            link = browser.current_url
            links.append(link)
            sleep(1)
            stock_availability.append("Available")
        page_num = page_num + 1

    data = {"Product Name": names, "Price": prices, "Product Link": links, "Stock Availability": stock_availability}
    df = pd.DataFrame.from_dict(data, orient='index')
    df = df.transpose()
    df.to_csv("scraped_data.csv", index=False)
    print("Scraping completed successfully!")

if __name__ == "__main__":
    main()
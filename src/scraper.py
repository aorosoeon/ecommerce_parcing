import pandas as pd
import csv
import traceback
from login_info import optanon_alert_box_closed, optanon_consent, ss_user_id, url
from time import sleep
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

service = Service(executable_path="/Users/arsenchuzhykov/Desktop/fastapi/chromedriver") #creating Service object for handling the browser driver
browser = webdriver.Chrome(service=service) #creating a new instance of chromedriver

def get_initial_window(): #pulling up initial Chrome window, the logic here might seem complicated, but it's the best combination of steps I've seen so far (for example, if you insert cookies, and then open url - everything crashes)
    browser.get(url)
    sleep(2) #sleeps are here for creating smoother flow and as a double check that everything is loaded
    browser.add_cookie({"name": "ssUserId", "value": ss_user_id}) #adding cookies so any pop up windows don't bother us
    browser.add_cookie({"name": "OptanonConsent", "value": optanon_consent})
    browser.add_cookie({"name": "OptanonAlertBoxClosed", "value": optanon_alert_box_closed})
    sleep(2)
    browser.get(url) #here the page is without any banners
    sleep(5)
    WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body"))) #"wait until" to ensure it's loaded

def log_exception_to_csv(part, error_message, stack_trace):
    log_file = "error_log.csv"
    with open(log_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([part, error_message, stack_trace, str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))])

def main():
    try: #try except block for exception handling in main
        get_initial_window()
        names, prices, links, stock_availability = [], [], [], []
        page_num = 1
        while page_num < 4: #limiting to just a couple pages for a demonstration purpose, REMOVE if needed
            try: #try except block for exception handling in pagination
                browser.get(f"{url}?page={page_num}")
                sleep(5)
                product_links = [link.get_attribute("href") for link in browser.find_elements(By.TAG_NAME, "a") if link.get_attribute("class") == "product-item-link ng-binding"]
                for product_link in product_links[1:3]: #limiting to just a couple items for a demonstration purpose, REMOVE if needed
                    try: #try except block for exception handling in items
                        browser.get(product_link)
                        sleep(5)
                        WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                        product_name_element = browser.find_element(By.XPATH, "//span[@data-ui-id='page-title-wrapper']") #finding individual element - in this case product's name
                        names.append(product_name_element.text)
                        product_price_element = browser.find_element(By.XPATH, "//span[@class='price']")
                        prices.append(product_price_element.text)
                        link = browser.current_url
                        links.append(link)
                        stock_availability.append("Available") #just for this case, since all the products on that website are available
                    except Exception as e:
                        log_exception_to_csv("item", str(e), traceback.format_exc())
                page_num = page_num + 1 #switching page
            except Exception as e:
                log_exception_to_csv("page", str(e), traceback.format_exc())
        data = {"Product Name": names, "Price": prices, "Product Link": links, "Stock Availability": stock_availability}
        df = pd.DataFrame.from_dict(data, orient='index')
        df = df.transpose()
        df.to_csv("scraped_data.csv", index=False) #updating csv
        print("Scraping completed successfully!")
    except Exception as e:
        log_exception_to_csv("main function", str(e), traceback.format_exc())

if __name__ == "__main__": #safeguard
    main()

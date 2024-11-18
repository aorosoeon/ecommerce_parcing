#----------THESE FUNCTIONS WERE USED IN EARLIER VERSIONS WITH A DIFFERENT PAGINATION HANDLING LOGIC----------
#----------SAVING THEM HERE IN CASE I NEED TO SWITCH TO PREVIOUS METHOD----------
"""
def js_click(browser, button, seconds): #clicking with javascript is more reliable
    WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body"))) #making sure that the page is loaded. if it's not and you will try to click, the program will crash
    browser.execute_script("arguments[0].click();", button) #clicking the element with javascript
    sleep(seconds) #wait to ensure that there is a pause between click and next action

def next_page(): #changing page
    next_page = browser.find_element(By.XPATH, "//a[@class='action  next' and contains(@ng-href, 'https://www.sail.ca/en/footwear/men?page=')]")
    js_click(browser, next_page, 2)
    sleep(4)
    WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    browser.back() #going to previous page
    sleep(4)
"""

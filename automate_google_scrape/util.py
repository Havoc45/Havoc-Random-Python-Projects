from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

#this function checks if the number of dork arguments are correct
def valid_statement(mydic):
    benchmark = len(mydic['-o'])
    if len(mydic['-k']) == 1+benchmark and len(mydic['-d']) == 1 + benchmark:
        return None
    else:
        raise Exception("invalid number of dorks & keywords to operators")

#this function waits until we see the first result of the google search
def wait_until(browser):
    try:
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "g"))
        )
    except:
        browser.quit()
        raise Exception('browser timed out after 10 seconds, google may have blocked your IP from using dorks')

#this function moves the browser to google then executes the search_string
def execute_g_search(browser,search_string):
    try:
        browser.get("https://www.google.com")
        element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
    except:
        browser.quit()
        raise Exception('Chrome browser timed out after 10 seconds, google may have blocked your IP from using dorks')
    else:
        try:
            search = browser.find_element_by_name('q')
            search.send_keys(search_string)
            search.send_keys(Keys.RETURN)
        except Exceptions as e:
            raise e

def web_suffix_handler(mystr):
    suffix = ['.gov','.org','.net','.com']
    while len(suffix) != 0:
        target = suffix.pop()
        trim = mystr.find(target)
        if trim != -1:
            return trim
    trim = None
    return trim

#print('no error in util')

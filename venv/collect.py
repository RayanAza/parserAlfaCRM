from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from pandas import read_html
from pygsheets import authorize


def login(driver: webdriver, username, password):
    login_url = 'https://royalacetennisclub.s20.online/'
    driver.get(login_url)

    # Find the username and password input fields using their IDs and fill them in
    username_input = driver.find_element(By.ID, 'loginform-username')
    password_input = driver.find_element(By.ID, 'loginform-password')

    username_input.send_keys(username)
    password_input.send_keys(password)

    # You can also simulate pressing the 'Enter' key to submit the form
    password_input.send_keys(Keys.ENTER)

    # If the website has a login button, you can click it instead of simulating 'Enter'
    # login_button = driver.find_element_by_id('login-button-id')
    # login_button.click()

    # Optionally, you can wait for a moment to see if the login is successful
    driver.implicitly_wait(5)
    return True

def next_page(driver: webdriver) -> bool:
    try:
        # Find the "Next" button in the pagination and click on the associated "a" tag
        pagination_list = driver.find_element(By.CLASS_NAME, 'pagination')
        next_button = pagination_list.find_element(By.CLASS_NAME, 'next')
        next_button_a = next_button.find_element(By.TAG_NAME, 'a')
        next_button_a.click()
        return True
    except:
        print('You are already on the last page')
        return False

def get_dataframe(driver: webdriver):
    table_data = driver.find_element(By.CLASS_NAME, 'crm-table')
    table_html = table_data.get_attribute('outerHTML')

    df = read_html(table_html)[0]

    return df

def upload_to_google_sheet(service_file_path, page_url, df, number_of_page: int) -> None:
    gc = authorize(service_file=service_file_path)
    spreadsheet = gc.open_by_url(page_url)

    sheet = spreadsheet[number_of_page]

    sheet.clear()

    sheet.set_dataframe(df, start='A1')

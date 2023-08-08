from venv.collect import login, next_page, get_dataframe, upload_to_google_sheet
from venv.reduction import reduction_clients, reduction_transactions, reduction_groups
from authorization.user import USERNAME, PASSWORD
from selenium import webdriver
from time import sleep
from pandas import concat



def parsing_clients(username=USERNAME, password=PASSWORD):
    driver = webdriver.Firefox()
    
    if login(driver, username, password):
        sleep(3)
        driver.get(r'https://royalacetennisclub.s20.online/company/1/customer/index')
        
        source = reduction_clients(get_dataframe(driver))
        print("Have finished 1 page...")
        i = 2
        while next_page(driver):
            sleep(2)
            source = concat([source, reduction_clients(get_dataframe(driver))])
            print(f"Have finished {i} page...")
            i += 1

        with open('.\\data\\clients.json', 'w', encoding='utf-8') as file:
            source.to_json(file, orient='table', force_ascii=False)
        
        upload_to_google_sheet(service_file_path='.\\authorization\\cred.json', 
                               page_url='https://docs.google.com/spreadsheets/d/1IxjBLSUHA5VQoWouFJ9_stmCyEOpgXE6uab9zVGh1IQ', 
                               df=source, number_of_page=0)
        
def parsing_clients_archive(username=USERNAME, password=PASSWORD):
    driver = webdriver.Firefox()
    
    if login(driver, username, password):
        sleep(3)
        driver.get(r'https://royalacetennisclub.s20.online/company/1/customer/index?CustomerSearch%5Bf_removed%5D=2') 
        source = reduction_clients(get_dataframe(driver))
        print("Have finished 1 page...")

        i = 2
        while next_page(driver):
            sleep(2)
            source = concat([source, reduction_clients(get_dataframe(driver))])
            print(f"Have finished {i} page...")
            i += 1
        
        with open('.\\data\\clients_archive.json', 'w', encoding='utf-8') as file:
            source.to_json(file, orient='table', force_ascii=False)
        
        upload_to_google_sheet(service_file_path='.\\authorization\\cred.json', 
                               page_url='https://docs.google.com/spreadsheets/d/1IxjBLSUHA5VQoWouFJ9_stmCyEOpgXE6uab9zVGh1IQ', 
                               df=source, number_of_page=1)

def parsing_finance(username=USERNAME, password=PASSWORD):
    driver = webdriver.Firefox()
    if login(driver, username, password):
        sleep(3)
        driver.get(r'https://royalacetennisclub.s20.online/company/1/pay/index')

        source = reduction_transactions(get_dataframe(driver))
        print("Have finished 1 page...")
        i = 2
        while next_page(driver):
            sleep(2)
            source = concat([source, reduction_transactions(get_dataframe(driver))])
            print(f"Have finished {i} page...")
            i += 1

        with open('.\\data\\transactions.json', 'w', encoding='utf-8') as file:
            source.to_json(file, orient='table', force_ascii=False)
        
        upload_to_google_sheet(service_file_path='.\\authorization\\cred.json', 
                               page_url='https://docs.google.com/spreadsheets/d/1IxjBLSUHA5VQoWouFJ9_stmCyEOpgXE6uab9zVGh1IQ', 
                               df=source, number_of_page=2)
        
def parsing_groups(username=USERNAME, password=PASSWORD):
    driver = webdriver.Firefox()
    if login(driver, username, password):
        sleep(3)
        driver.get(r'https://royalacetennisclub.s20.online/company/1/group/index')

        source = reduction_groups(get_dataframe(driver))
        print("Have finished 1 page...")
        i = 2
        while next_page(driver):
            sleep(2)
            source = concat([source, reduction_groups(get_dataframe(driver))])
            print(f"Have finished {i} page...")
            i += 1

        with open('.\\data\\groups.json', 'w', encoding='utf-8') as file:
            source.to_json(file, orient='table', force_ascii=False)
        
        upload_to_google_sheet(service_file_path='.\\authorization\\cred.json', 
                               page_url='https://docs.google.com/spreadsheets/d/1IxjBLSUHA5VQoWouFJ9_stmCyEOpgXE6uab9zVGh1IQ', 
                               df=source, number_of_page=3)
        
if __name__ == '__main__':
    # use needed functions
    pass
    

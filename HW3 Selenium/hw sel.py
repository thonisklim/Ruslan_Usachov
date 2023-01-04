from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
import time

username = 'Admin'
password = 'admin123'
name = 'NotRandomName'
hardpass = 'Hardpassw0rd+'
min_sal = 2000
max_sal = 20000
curr_name = 'UAH'

url = "https://opensource-demo.orangehrmlive.com/"
driver = webdriver.Chrome()
driver.maximize_window()
driver.get(url=url)
wait = WebDriverWait(driver, 5)
# logging in
wait.until(ec.visibility_of_element_located((By.XPATH, "//input[@name='username']"))).send_keys(username)
driver.find_element(By.XPATH, "//input[@name='password']").send_keys(password)
driver.find_element(By.XPATH, "//button[@type='submit']").click()
# on the main page
wait.until(ec.visibility_of_element_located((By.XPATH, "//a[contains(.,'Admin')]"))).click()
wait.until(ec.visibility_of_element_located((By.XPATH, "//span[contains(.,'Job ')]"))).click()
wait.until(ec.visibility_of_element_located((By.XPATH, "//a[contains(.,'Pay Grades')]"))).click()
# add new RandomName
wait.until(ec.visibility_of_element_located((By.XPATH, "//button[contains(.,' Add ')]"))).click()
wait.until(ec.visibility_of_element_located((By.XPATH, '//div[2]/input'))).send_keys(name)
wait.until(ec.visibility_of_element_located((By.XPATH, "//button[@type='submit']"))).click()
# fill up Currencies
wait.until(ec.visibility_of_element_located((By.XPATH, "//button[contains(.,' Add ')]"))).click()
wait.until(ec.visibility_of_element_located((By.XPATH, '//div[@class="oxd-select-text-input"]'))).click()
wait.until(ec.visibility_of_element_located((By.XPATH, f'//div[@class="oxd-select-option" and contains(.,"{curr_name}")]'))).click()
# have to use terrible xpath because of same classes of inputs and buttons "save"
wait.until(ec.visibility_of_element_located((By.XPATH, '(//input[@class="oxd-input oxd-input--active"])[3]'))).send_keys(min_sal)
wait.until(ec.visibility_of_element_located((By.XPATH, '(//input[@class="oxd-input oxd-input--active"])[3]'))).send_keys(max_sal)
wait.until(ec.visibility_of_element_located((By.XPATH, '(//button[@type="submit"])[2]'))).click()
wait.until(ec.visibility_of_element_located((By.XPATH, '//button[@type="submit"]'))).click()
# delete currencies
del_curr = f'//div[@class="oxd-table-cell oxd-padding-cell" and contains(.,"{min_sal}")]' \
           f'//following-sibling::div/descendant::i[@class="oxd-icon bi-trash"]'
wait.until(ec.visibility_of_element_located((By.XPATH, del_curr))).click()
wait.until(ec.visibility_of_element_located((By.XPATH, "//button[contains(.,' Yes, Delete')]"))).click()
time.sleep(5)
# delete row
wait.until(ec.visibility_of_element_located((By.XPATH, "//button[contains(.,'Cancel')]"))).click()
del_row = f'//div[@class="oxd-table-cell oxd-padding-cell" and contains(.,"{name}")]' \
          f'//following-sibling::div/descendant::i[@class="oxd-icon bi-trash"]'
time.sleep(5)
wait.until(ec.visibility_of_element_located((By.XPATH, del_row))).click()
wait.until(ec.visibility_of_element_located((By.XPATH, "//button[contains(.,' Yes, Delete')]"))).click()
time.sleep(10)
driver.close()

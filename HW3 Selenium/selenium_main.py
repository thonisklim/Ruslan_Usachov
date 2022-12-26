from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

username = 'Admin'
password = 'admin123'
name = 'Usachov_Ruslan'
hard_pass = 'Hardpassw0rd+'
part_name = 'Odis'


class TestVar1:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(url="https://opensource-demo.orangehrmlive.com/")
        self.wait = WebDriverWait(self.driver, 5)

    def log_in(self):
        self.wait.until(ec.visibility_of_element_located((By.XPATH, "//input[@name='username']"))).send_keys(username)
        self.driver.find_element(By.XPATH, "//input[@name='password']").send_keys(password)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

    def main_page(self):
        self.wait.until(ec.visibility_of_element_located((By.XPATH, "//a[contains(.,'Admin')]"))).click()

    # adding row
    def add_row(self):
        self.wait.until(ec.visibility_of_element_located((By.XPATH, "//button[contains(.,' Add ')]"))).click()
        self.wait.until(ec.visibility_of_element_located(
            (By.XPATH, '(//input[@class="oxd-input oxd-input--active"])[2]'))).send_keys(name)
        self.driver.find_element(By.XPATH, "//input[@type='password']").send_keys(hard_pass)
        self.driver.find_element(By.XPATH, "(//input[@type='password'])[2]").send_keys(hard_pass)
        self.driver.find_element(By.XPATH, '//div[@class="oxd-autocomplete-wrapper"]'
                                           '/descendant::input').send_keys(part_name)
        self.wait.until(ec.visibility_of_element_located((By.XPATH, f'//div[@class="oxd-autocomplete-option" and '
                                                                    f'contains(.,"{part_name}")]'))).click()
        self.wait.until(ec.visibility_of_element_located((By.XPATH, '//div[@class="oxd-select-wrapper" and '
                                                                    'contains(.,"-- Select --")]'))).click()
        self.wait.until(ec.visibility_of_element_located((By.XPATH, '//div[@class="oxd-select-option" and '
                                                                    'contains(.,"ESS")]'))).click()
        self.wait.until(ec.visibility_of_element_located((By.XPATH, '//div[@class="oxd-select-wrapper" and '
                                                                    'contains(.,"-- Select --")]'))).click()
        self.wait.until(ec.visibility_of_element_located((By.XPATH, '//div[@class="oxd-select-option" and '
                                                                    'contains(.,"Enabled")]'))).click()
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

    def find_my_row(self):
        self.wait.until(ec.visibility_of_element_located((By.XPATH, '//button[contains(.,"Reset")]'))).click()
        self.wait.until(ec.visibility_of_element_located((By.XPATH, '(//input[@class="oxd-input '
                                                                    'oxd-input--active"])[2]'))).send_keys(name)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()

    def delete_my_row(self):
        del_row = f'//div[@class="oxd-table-row oxd-table-row--with-border" and contains(.,"{name}")]' \
                  f'//following-sibling::div/descendant::i[@class="oxd-icon bi-trash"]'
        self.wait.until(ec.visibility_of_element_located((By.XPATH, del_row))).click()
        self.wait.until(ec.visibility_of_element_located((By.XPATH, "//button[contains(.,' Yes, Delete')]"))).click()
        self.driver.close()

    def dotest(self):
        self.log_in()
        self.main_page()
        self.add_row()
        self.find_my_row()
        self.delete_my_row()


test = TestVar1()
test.dotest()

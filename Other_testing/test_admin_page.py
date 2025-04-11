import os
import time  # Import time for adding delays
from dotenv import load_dotenv
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

load_dotenv(override=True)
username = os.getenv("ADMIN_USERNAME")
password = os.getenv("ADMIN_PASSWORD")

@pytest.fixture(scope="class")
def setup(request):
    driver = webdriver.Chrome()
    driver.maximize_window()
    request.cls.driver = driver
    yield
    driver.quit()

@pytest.mark.usefixtures("setup")
class TestadminPanel:
    base_url = "https://www.hireskilldev.com/auth/signin"

    def wait_for_element(self, by, value, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by,value))
        )
    
    def test_01_valid_login(self):
        self.driver.get(self.base_url)

        email_field = self.wait_for_element(By.XPATH, "//*[@id='email']")
        password_field = self.wait_for_element(By.XPATH, "//*[@id='password']")
        login_button = self.wait_for_element(By.XPATH, "//*[@id='root']/div[2]/div/form/button")

        email_field.send_keys("admin2@gmail.com")  
        password_field.send_keys("admin2@gmail.com")
        login_button.click()

        dashboard = self.wait_for_element(By.XPATH, "/html/body/div/div[2]/div/aside/div/div/a[1]")  
        assert dashboard is not None, "Login failed!"
    
    def test_02_all_candidates_page(self):

        self.driver.get("https://www.hireskilldev.com/admin/candidate")

        all_candidates_button = self.wait_for_element(By.XPATH, "/html/body/div/div[2]/div/aside/div/div/a[3]")
        all_candidates_button.click()

        time.sleep(2)

        acp_component = self.wait_for_element(By.XPATH, "/html/body/div/div[2]/div/div/div/section[3]/div/div[1]/div/table/tbody/tr[1]/td[6]/button")

        time.sleep(2)

        assert acp_component is not None, "Candidate Page Failed to Load"


        acp_component.click()
        acp_component_menu = self.wait_for_element(By.XPATH, "/html/body/div[2]/div/div[4]")
        acp_component_menu.click()
        time.sleep(10)

    def test_03_test_report_page(self):

        self.driver.get("https://www.hireskilldev.com/admin/candidate/e258ac67-9b4b-4bd0-b8f1-929e53c68012/report")

        view_button = self.wait_for_element(By.XPATH, "/html/body/div/div[2]/div/div/div/section[1]/div/div/div[1]/div/table/tbody/tr[1]/td[5]/button")
        view_button.click()

        time.sleep(3)
        tr_compo = self.wait_for_element(By.XPATH, "/html/body/div/main/main/div/h1")
        assert tr_compo is not None, "Failed to load Report"

        time.sleep(10)
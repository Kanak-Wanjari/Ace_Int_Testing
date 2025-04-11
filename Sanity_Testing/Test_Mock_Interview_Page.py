import os
from dotenv import load_dotenv
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

load_dotenv(override=True)
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

@pytest.fixture(scope="class")
def setup(request):
    chrome_options = webdriver.ChromeOptions()
    
    # Automatically allow camera and microphone access
    chrome_options.add_argument("--use-fake-ui-for-media-stream")
    
    # Optional: Disable popups for a smoother experience
    chrome_options.add_argument("--disable-popup-blocking")
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    request.cls.driver = driver
    yield
    driver.quit()

    # driver = webdriver.Chrome()
    # driver.maximize_window()
    # request.cls.driver = driver
    # yield
    # driver.quit()

@pytest.mark.usefixtures("setup")
class TestMockAI:

    # base_url = "https://www.hireskilldev.com/auth/signin"

    def wait_for_element(self,by,value, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
    
    def test_01_valid_login(self):
        """Test case for valid login credentials."""
        self.driver.get("https://www.hireskilldev.com/auth/signin")

        email_field = self.wait_for_element(By.XPATH, "//*[@id='email']")
        password_field = self.wait_for_element(By.XPATH, "//*[@id='password']")
        login_button = self.wait_for_element(By.XPATH, "//*[@id='root']/div[2]/div/form/button")

        email_field.send_keys(username)  
        password_field.send_keys(password)
        login_button.click()

        # Verify dashboard access
        dashboard = self.wait_for_element(By.XPATH, "//*[@id='root']/main/main/aside/div/div[1]/a[2]/h1")  
        assert dashboard is not None, "Login failed!"

    def test_02_mock_test_page_load(self):
        self.driver.get("https://www.hireskilldev.com/mock-test")

        mock_test_page_button = self.wait_for_element(By.XPATH, "/html/body/div/main/main/aside/div/div[1]/a[3]")
        mock_test_page_button.click()

        time.sleep(3)

        mock_test_compo = self.wait_for_element(By.XPATH, "/html/body/div/main/main/div/div/section/div/div/div/div[1]/div/div[2]/h1")

        assert mock_test_compo is not None, "Mock Test Page Load Failed"

    def test_03_mock_test_loading(self):

        self.driver.get("https://www.hireskilldev.com/mock-test")

        load_mock_test_button = self.wait_for_element(By.XPATH, "/html/body/div/main/main/div/div/section/div/div/div/div[1]/div/div[2]/h1")
        load_mock_test_button.click()

        time.sleep(3)

        enroll_now_button = self.wait_for_element(By.XPATH, "/html/body/div/main/main/div/div/section/button")
        assert enroll_now_button is not None, "Mock test page loading Failed"
        enroll_now_button.click()

        enroll_now_button_1 = self.wait_for_element(By.XPATH, "/html/body/div[3]/div[2]/button")
        enroll_now_button_1.click()

        time.sleep(3)

        start_test_button = self.wait_for_element(By.XPATH, "/html/body/div/main/main/div/div/section/button")
        start_test_button.click()

        time.sleep(2)

        start_test_button_1 = self.wait_for_element(By.XPATH, "/html/body/div[3]/div[3]/button")
        assert start_test_button_1 is not None, "Guidelines page not Loaded"
        start_test_button_1.click()
        
        time.sleep(5)

        submit_button = self.wait_for_element(By.XPATH, "/html/body/div/div[2]/div/div/div/div[2]/div/div[3]/button")
        assert submit_button is not None , "Mock test Loading Failed"

        time.sleep(10)

        submit_button.click()

        confirm_submission_button = self.wait_for_element(By.XPATH, "/html/body/div/div[2]/div/div/div/div[2]/div/div[3]/div/div/div/div[2]/button[2]")
        confirm_submission_button.click()

        time.sleep(12)

        view_full_report_button = self.wait_for_element(By.XPATH, "/html/body/div/main/main/div/div/div/div[1]/button")
        assert view_full_report_button is not None, "Report Loading Failed"
        view_full_report_button.click()

        time.sleep(5)

        test_report_compo = self.wait_for_element(By.XPATH, "/html/body/div/main/main/div/div/div/div/section[2]/div[1]/div/h1")
        assert test_report_compo is not None, "Test report failed to Load"

        time.sleep(5)
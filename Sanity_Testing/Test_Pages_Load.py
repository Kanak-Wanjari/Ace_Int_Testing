import os
from dotenv import load_dotenv
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv(override=True)
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

@pytest.fixture(scope="class")

def setup(request):
    """Setup Webdriver"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    request.cls.driver = driver
    yield
    driver.quit()

@pytest.mark.usefixtures("setup")

class TestAIInterview:

    base_url = "https://www.aceint.ai/auth/signin"

    def wait_for_element(self, by, value, timeout=10):
        """Wait for element to appear with timeout handling."""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by,value))
        )
    
    def test_01_valid_login(self):
        """Test case for valid login credentials."""
        self.driver.get(self.base_url)

        email_field = self.wait_for_element(By.XPATH, "//*[@id='email']")
        password_field = self.wait_for_element(By.XPATH, "//*[@id='password']")
        login_button = self.wait_for_element(By.XPATH, "//*[@id='root']/div[2]/div/form/button")

        email_field.send_keys(username)  # Use env vars directly
        password_field.send_keys(password)
        login_button.click()

        # Verify dashboard access
        dashboard = self.wait_for_element(By.XPATH, "//*[@id='root']/main/main/aside/div/div[1]/a[2]/h1")
        assert dashboard is not None, "Login failed!"
    
    def test_02_ai_interview_page_load(self):

        self.driver.get("https://www.aceint.ai/ai-interview")

        ai_int_compo_1 = self.wait_for_element(By.XPATH, "//*[@id='root']/main/main/div/div/div[2]/section/button[1]/div/div[1]/div[2]")
        ai_int_compo_2 = self.wait_for_element(By.XPATH, "//*[@id='root']/main/main/div/div/div[2]/section/button[2]/div/div[1]/div[2]")

        assert ai_int_compo_1 is not None, "Interview page load failed"
        assert ai_int_compo_2 is not None, "Interview page load failed"

    def test_03_ai_mock_test_page_load(self):

        self.driver.get("https://www.aceint.ai/mock-test")

        ai_mock_compo_1 = self.wait_for_element(By.XPATH, "//*[@id='root']/main/main/div/div/section/div/div/div/div[1]/div/div[2]/h1")
        ai_mock_compo_2 = self.wait_for_element(By.XPATH, "//*[@id='root']/main/main/div/div/section/div/div/div/div[2]/div/div[2]/h1")

        assert ai_mock_compo_1 is not None, "Mock test Page load Failed"
        assert ai_mock_compo_2 is not None, "Mock test Page load Failed"
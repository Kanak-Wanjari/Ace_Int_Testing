import os
from dotenv import load_dotenv
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load environment variables
load_dotenv(override=True)
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

@pytest.fixture(scope="class")
def setup(request):
    """Setup WebDriver"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    request.cls.driver = driver
    yield
    driver.quit()

@pytest.mark.usefixtures("setup")
class TestLogin:

    base_url = "https://www.aceint.ai/auth/signin"  # Replace with your actual URL

    def wait_for_element(self, by, value, timeout=10):
        """Wait for element to appear with timeout handling."""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def test_01_empty_fields(self):
        """Test case for both fields empty."""
        self.driver.get(self.base_url)

        login_button = self.wait_for_element(By.XPATH, "//*[@id='root']/div[2]/div/form/button")
        login_button.click()

        error_message = self.wait_for_element(By.XPATH, "//*[@id='root']/div[2]/div/form/div[1]")
        assert error_message is not None, "Error message not shown!"

    def test_02_missing_email(self):
        """Test case for missing email."""
        self.driver.get(self.base_url)

        password_field = self.wait_for_element(By.XPATH, "//*[@id='password']")
        login_button = self.wait_for_element(By.XPATH, "//*[@id='root']/div[2]/div/form/button")

        password_field.send_keys(password)  # Use the env var directly
        login_button.click()

        error_message = self.wait_for_element(By.XPATH, "//*[@id='root']/div[2]/div/form/div[1]")
        assert error_message is not None, "Error message not shown!"

    def test_03_missing_password(self):
        """Test case for missing password."""
        self.driver.get(self.base_url)

        email_field = self.wait_for_element(By.XPATH, "//*[@id='email']")
        login_button = self.wait_for_element(By.XPATH, "//*[@id='root']/div[2]/div/form/button")

        email_field.send_keys(username)  # Use the env var directly
        login_button.click()

        error_message = self.wait_for_element(By.XPATH, "//*[@id='root']/div[2]/div")
        assert error_message is not None, "Error message not shown!"

    def test_04_invalid_login(self):
        """Test Case for Invalid Login Credentials"""
        self.driver.get(self.base_url)

        email_field = self.wait_for_element(By.XPATH, "//*[@id='email']")
        password_field = self.wait_for_element(By.XPATH, "//*[@id='password']")
        login_button = self.wait_for_element(By.XPATH, "//*[@id='root']/div[2]/div/form/button")

        email_field.send_keys("Kanak@gmail.com")  # Use env vars directly
        password_field.send_keys("kanak2341@")
        login_button.click()

        error_message = self.wait_for_element(By.XPATH, "//*[@id='root']/div/div/div[2]")
        assert error_message is not None, "Error message not shown!"

    def test_05_valid_login(self):
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
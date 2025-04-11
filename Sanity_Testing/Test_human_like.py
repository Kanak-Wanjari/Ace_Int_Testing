import os
import time
import random
from dotenv import load_dotenv
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

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
    base_url = "https://www.hireskilldev.com/auth/signin"

    def wait_for_element(self, by, value, timeout=10):
        """Wait for element to appear with timeout handling."""
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def human_like_delay(self, min_time=1, max_time=3):
        """Introduce random human-like delay."""
        time.sleep(random.uniform(min_time, max_time))

    def human_like_click(self, element):
        """Simulate human-like mouse movements and click."""
        actions = ActionChains(self.driver)
        actions.move_to_element(element).pause(random.uniform(0.5, 1.5)).click().perform()
        self.human_like_delay(1, 3)

    def human_like_typing(self, element, text, min_delay=0.1, max_delay=0.5):
        """Simulate human-like typing with variable delays."""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(min_delay, max_delay))

    def test_01_valid_login(self):
        """Test case for valid login credentials."""
        self.driver.get(self.base_url)
        self.human_like_delay(2, 4)

        # Fields
        email_field = self.wait_for_element(By.XPATH, "//*[@id='email']")
        password_field = self.wait_for_element(By.XPATH, "//*[@id='password']")
        login_button = self.wait_for_element(By.XPATH, "//*[@id='root']/div[2]/div/form/button")

        # Human-like interactions
        self.human_like_typing(email_field, username)
        self.human_like_delay(1, 2)

        self.human_like_typing(password_field, password)
        self.human_like_delay(2, 4)

        self.human_like_click(login_button)

        # Verify dashboard access
        dashboard = self.wait_for_element(By.XPATH, "//*[@id='root']/main/main/aside/div/div[1]/a[2]/h1")
        assert dashboard is not None, "Login failed!"

    def test_02_ai_interview_page_load(self):
        """Test case to verify AI interview page loads properly."""
        self.driver.get("https://www.hireskilldev.com/ai-interview")
        self.human_like_delay(2, 4)

        ai_int_compo_1 = self.wait_for_element(By.XPATH, "//*[@id='root']/main/main/div/div/div[2]/section/button[1]/div/div[1]/div[2]")
        ai_int_compo_2 = self.wait_for_element(By.XPATH, "//*[@id='root']/main/main/div/div/div[2]/section/button[2]/div/div[1]/div[2]")

        self.human_like_click(ai_int_compo_1)
        self.human_like_delay(2, 4)

        self.human_like_click(ai_int_compo_2)

        assert ai_int_compo_1 is not None, "Interview page load failed"
        assert ai_int_compo_2 is not None, "Interview page load failed"

    def test_03_ai_int_pop_up_load(self):
        """Test case to verify pop-up loads properly."""
        self.driver.get("https://www.hireskilldev.com/ai-interview")
        self.human_like_delay(2, 4)

        ai_int_compo_3 = self.wait_for_element(By.XPATH, "//*[@id='root']/main/main/div/div/div[2]/section/button[1]/div/div[1]/div[2]")
        self.human_like_click(ai_int_compo_3)

        # Job Role Selection
        job_role_button = self.wait_for_element(By.XPATH, "/html/body/div[3]/div/form/label[1]/button")
        self.human_like_click(job_role_button)

        job_role = self.wait_for_element(By.XPATH, "/html/body/div[3]/div/form/label[1]/select/option[11]")
        self.human_like_click(job_role)

        # Interview Type Selection
        interview_type_button = self.wait_for_element(By.XPATH, "/html/body/div[3]/div/form/label[2]/button")
        self.human_like_click(interview_type_button)

        interview_type = self.wait_for_element(By.XPATH, "/html/body/div[3]/div/form/label[2]/select/option[2]")
        self.human_like_click(interview_type)

        # Interview Duration Selection
        interview_duration_button = self.wait_for_element(By.XPATH, "/html/body/div[3]/div/form/label[2]/button")
        self.human_like_click(interview_duration_button)

        interview_duration = self.wait_for_element(By.XPATH, "/html/body/div[3]/div/form/label[2]/select/option[2]")
        self.human_like_click(interview_duration)

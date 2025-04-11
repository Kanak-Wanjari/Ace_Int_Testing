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
    
    def test_01_valid_login(self):
        """Test case for valid login credentials."""
        self.driver.get(self.base_url)

        email_field = self.wait_for_element(By.XPATH, "//*[@id='email']")
        password_field = self.wait_for_element(By.XPATH, "//*[@id='password']")
        login_button = self.wait_for_element(By.XPATH, "//*[@id='root']/div[2]/div/form/button")

        email_field.send_keys(username)  
        password_field.send_keys(password)
        login_button.click()

        # Verify dashboard access
        dashboard = self.wait_for_element(By.XPATH, "//*[@id='root']/main/main/aside/div/div[1]/a[2]/h1")  
        assert dashboard is not None, "Login failed!"
    
    def test_02_ai_interview_page_load(self):
        """Test case to verify AI interview page loads successfully."""
        self.driver.get("https://www.hireskilldev.com/ai-interview")

        ai_int_compo_1 = self.wait_for_element(By.XPATH, "//*[@id='root']/main/main/div/div/div[2]/section/button[1]/div/div[1]/div[2]")
        ai_int_compo_2 = self.wait_for_element(By.XPATH, "//*[@id='root']/main/main/div/div/div[2]/section/button[2]/div/div[1]/div[2]")

        assert ai_int_compo_1 is not None, "Interview page load failed"
        assert ai_int_compo_2 is not None, "Interview page load failed"

    def test_03_ai_int_pop_up_load(self):
        """Test case for verifying AI interview pop-up loads correctly."""
        self.driver.get("https://www.hireskilldev.com/ai-interview")

        search_box_button = self.wait_for_element(By.XPATH, "/html/body/div/main/main/div/div/section/div/input")
        search_box_button.send_keys("DXC")

        time.sleep(1)

        ai_int_compo_3 = self.wait_for_element(By.XPATH, "//*[@id='root']/main/main/div/div/div[2]/section/button[1]/div/div[1]/div[2]")
        ai_int_compo_3.click()

        job_role_button = self.wait_for_element(By.XPATH, "/html/body/div[3]/div/form/label[1]/button")     
        job_role_button.click()
        time.sleep(1)  # Pause to let options load
        job_role = self.wait_for_element(By.XPATH, "/html/body/div[3]/div/form/label[1]/select/option[11]")
        job_role.click()

        interview_type_button = self.wait_for_element(By.XPATH, "/html/body/div[3]/div/form/label[2]/button")
        interview_type_button.click()
        time.sleep(1)
        interview_type = self.wait_for_element(By.XPATH, "/html/body/div[3]/div/form/label[2]/select/option[2]")
        interview_type.click()

        interview_duration_button = self.wait_for_element(By.XPATH, "/html/body/div[3]/div/form/label[3]/button")
        interview_duration_button.click()
        time.sleep(1)  # Pause to let options load

        interview_duration_select = self.wait_for_element(By.XPATH, "/html/body/div[3]/div/form/label[3]/select")

        # Use Selenium's Select class to select the option
        select = Select(interview_duration_select)
        select.select_by_index(1)

        # interview_duration = self.wait_for_element(By.XPATH, "/html/body/div[3]/div/form/label[3]/select/option[1]")    
        # interview_duration.click()

        interview_difficulty_button = self.wait_for_element(By.XPATH, "/html/body/div[3]/div/form/label[4]/button")
        interview_difficulty_button.click()
        time.sleep(1)
        interview_difficulty = self.wait_for_element(By.XPATH, "//*[@id='radix-:r2:']/div/form/label[4]/select/option[2]")      
        interview_difficulty.click()

        technical_skills_button = self.wait_for_element(By.XPATH, "/html/body/div[3]/div/form/label[5]/div/div/input")
        technical_skills_button.click()
        time.sleep(1)  # Small pause to ensure input field is active
        technical_skills_button.send_keys("Python")
        technical_skills_button.send_keys(Keys.ENTER)
        time.sleep(1)  
        technical_skills_button.send_keys("Django")
        technical_skills_button.send_keys(Keys.ENTER)

        terms_and_condition_checkbox = self.wait_for_element(By.XPATH, "/html/body/div[3]/div/form/label[6]/button")
        terms_and_condition_checkbox.click()

        time.sleep(1)
        start_interview_button = self.wait_for_element(By.XPATH, "/html/body/div[3]/div/form/button")
        start_interview_button.click()

        time.sleep(1)

        lets_begin_button = self.wait_for_element(By.XPATH, "/html/body/div/div[2]/main/main/div/button")
        assert lets_begin_button is not None, "Interview Page Loading Failed"

        time.sleep(30)
        lets_begin_button.click()

        time.sleep(2)
        end_interview_button = self.wait_for_element(By.XPATH, "/html/body/div/div[2]/main/main/nav[2]/section/div[3]/span")
        assert end_interview_button is not None , "Final Interview Page Loading Failed"
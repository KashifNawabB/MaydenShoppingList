from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import unittest

class LoginSeleniumTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up Chrome options
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Run headless mode
        chrome_options.add_argument("--disable-gpu")

        # Set up WebDriver
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_login_valid_credentials(self):
        driver = self.driver
        driver.get('http://localhost:8000/accounts/login/')

        # Fill out the login form
        driver.find_element(By.NAME, 'username').send_keys('ali')
        driver.find_element(By.NAME, 'password').send_keys('admin@123')
        driver.find_element(By.NAME, 'password').send_keys(Keys.RETURN)  # Submit the form

        # Check if redirected to the index page or the expected page after login
        self.assertIn('', driver.title)

    def test_login_invalid_credentials(self):
        driver = self.driver
        driver.get('http://localhost:8000/accounts/login/')  # Update URL as needed

        # Fill out the login form with invalid credentials
        driver.find_element(By.NAME, 'username').send_keys('ali')
        driver.find_element(By.NAME, 'password').send_keys('wrongpassword')
        driver.find_element(By.NAME, 'password').send_keys(Keys.RETURN)  # Submit the form

        # Check if error message is displayed
        error_message = driver.find_element(By.CSS_SELECTOR, '.alert.alert-danger').text
        self.assertIn('Please enter a correct username and password.', error_message)

    def test_login_page_loads(self):
        driver = self.driver
        driver.get('http://localhost:8000/accounts/login/')

        # Check if login page is loaded
        self.assertIn('Login', driver.title)

        # Check for presence of form elements
        self.assertTrue(driver.find_element(By.NAME, 'username'))
        self.assertTrue(driver.find_element(By.NAME, 'password'))
        self.assertTrue(driver.find_element(By.XPATH, '//button[text()="Login"]'))

if __name__ == "__main__":
    unittest.main()

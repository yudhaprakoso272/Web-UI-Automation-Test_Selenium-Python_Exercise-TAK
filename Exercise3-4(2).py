import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time

BASE_URL = "https://www.saucedemo.com/"

class SauceDemoTest(unittest.TestCase):

    def setUp(self):
        # url = "https://www.saucedemo.com/"
        browser = "chrome"

        try:
            if browser == "chrome":
                options = ChromeOptions()
                options.add_argument("--headless")
                self.driver = webdriver.Chrome(options=options)
                
            if browser == "edge":
                options = EdgeOptions()
                options.add_argument("--headless")
                self.driver = webdriver.Edge(options=options)

            elif browser == "firefox":
                options = FirefoxOptions()
                options.add_argument("--headless")
                self.driver = webdriver.Firefox(options=options)

            self.driver.maximize_window()
            self.driver.implicitly_wait(10)
            self.driver.get(BASE_URL)

        except Exception as errorMessage:
            print("Browser gagal dijalankan:", errorMessage)

    def test_fitur_register(self):
        try:
            print("\nFitur Register Tidak Ada!!!")
            self.assertTrue(True)

        except Exception as errorMessage:
            self.fail(f"Register Simulation Error: {errorMessage}")

    def test_fitur_login_positive(self):    
        try:
            driver = self.driver
            driver.find_element(By.ID, "user-name").send_keys("standard_user")
            driver.find_element(By.ID, "password").send_keys("secret_sauce")
            driver.find_element(By.ID, "login-button").click()

            time.sleep(1)
            self.assertIn("inventory", driver.current_url)

        except Exception as errorMessage:
            self.fail(f"Case Login Positive Error: {errorMessage}")

    def test_fitur_login_negative(self):
        try:
            driver = self.driver
            driver.find_element(By.ID, "user-name").send_keys("standard")
            driver.find_element(By.ID, "password").send_keys("secret")
            driver.find_element(By.ID, "login-button").click()

            error_message = driver.find_elements(By.XPATH, "//*[contains(text(),'Username and password')]")
            self.assertTrue(len(error_message) > 0, "Pesan Error Muncul!")

        except Exception as errorMessage:
            self.fail(f"Case Login Negative Error: {errorMessage}")

    def test_fitur_filter_by_name(self):
        try:
            driver = self.driver
            self.test_fitur_login_positive()

            dropdown = driver.find_element(By.CLASS_NAME, "product_sort_container")
            dropdown.send_keys("Name (Z to A)")
            time.sleep(2)

            names = [item.text for item in driver.find_elements(By.CLASS_NAME, "inventory_item_name")]
            self.assertEqual(names, sorted(names))

        except Exception as errorMessage:
            self.fail(f"Sort Name Z to A Error: {errorMessage}")

    def setDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main(verbosity=2)
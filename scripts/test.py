import time
import names
import random
import logging
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By


logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


class PrestaShopTest(unittest.TestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument('ignore-certificate-errors')

        self.driver = webdriver.Chrome(chrome_options=options)
        #self.driver = webdriver.Firefox()

    def test_prestashop(self):
        driver = self.driver
        driver.get("https://localhost:17188/")
        time.sleep(2.5)
        logging.info("Start filling a cart")
        self.fill_cart()
        logging.info("Remove random item from the cart")
        self.remove_from_cart()
        logging.info("register new account and order")
        order_id = self.register_and_order()
        logging.info(f"Order ID: {order_id}")
        logging.info("Check order status")
        self.check_status(order_id)

    def tearDown(self):
        self.driver.close()

    def fill_cart(self):
        top_menu = self.driver.find_element(By.ID, 'top-menu')
        categories = top_menu.find_elements(By.XPATH, "//ul[@id='top-menu' and @class='top-menu']/li")
        random_categories = random.sample(categories, 2)
        num_products_to_buy = [random.randint(1, 9)]
        num_products_to_buy.append(10 - num_products_to_buy[0])
        urls = list(map(lambda x: x.find_element(By.TAG_NAME, "a").get_property("href"), random_categories))
        for url, num in zip(urls, num_products_to_buy):
            logging.info(f"Category url: {url}")
            self.driver.get(url)
            time.sleep(2.5)
            products = self.driver.find_elements(By.XPATH, "//div[starts-with(@class, 'js-product product')]")
            random_products = random.sample(products, num)
            product_urls = list(map(lambda x: x.find_element(By.TAG_NAME, "a").get_property("href"), random_products))
            for product_url in product_urls:
                logging.info(f"Product url: {product_url}")
                self.driver.get(product_url)
                time.sleep(2.5)
                increase_quantity = random.randint(0, 10)
                increase_button = self.driver.find_element(By.XPATH, "//button[@class='btn btn-touchspin js-touchspin bootstrap-touchspin-up']")
                for _ in range(increase_quantity):
                    logging.info("Increasing quantity")
                    increase_button.click()
                    time.sleep(0.5)

                add_to_cart_button = self.driver.find_element(By.XPATH, "//button[@class='btn btn-primary add-to-cart']")
                add_to_cart_button.click()
                time.sleep(1)

    def remove_from_cart(self):
        self.driver.get("https://localhost:17188/koszyk?action=show")
        time.sleep(2.5)
        delete_button = random.choice(self.driver.find_elements(By.XPATH, "//a[@class='remove-from-cart']"))
        delete_button.click()
        time.sleep(1)

    def register_and_order(self):
        self.driver.get("https://localhost:17188/zamówienie")
        time.sleep(2.5)

        genders = self.driver.find_elements(By.XPATH, "//input[@name='id_gender']")
        gender_button = random.choice(genders)
        gender_button.click()
        time.sleep(1)

        first_name_field = self.driver.find_element(By.XPATH, "//input[@id='field-firstname']")
        first_name = names.get_first_name()
        first_name_field.send_keys(first_name)
        time.sleep(1)

        last_name_field = self.driver.find_element(By.XPATH, "//input[@id='field-lastname']")
        last_name = names.get_last_name()
        last_name_field.send_keys(last_name)
        time.sleep(1)

        email_field = self.driver.find_element(By.XPATH, "//input[@id='field-email']")
        email = f"{first_name}.{last_name}@mailsac.com"
        logging.info(f"Email used: {email}")
        email_field.send_keys(email)
        time.sleep(1)

        password_field = self.driver.find_element(By.XPATH, "//input[@id='field-password']")
        password_field.send_keys("haslohaslo")
        time.sleep(1)

        customer_privacy_checkbox = self.driver.find_element(By.XPATH, "//input[@name='customer_privacy']")
        customer_privacy_checkbox.click()
        time.sleep(1)

        privacy_policy_checkbox = self.driver.find_element(By.XPATH, "//input[@name='psgdpr']")
        privacy_policy_checkbox.click()
        time.sleep(1)

        continue_button = self.driver.find_element(By.XPATH, "//button[@class='continue btn btn-primary float-xs-right']")
        continue_button.click()
        time.sleep(1)

        address1_field = self.driver.find_element(By.XPATH, "//input[@id='field-address1']")
        address1_field.send_keys("ul. Spokojna 12")
        time.sleep(1)

        postcode_field = self.driver.find_element(By.XPATH, "//input[@id='field-postcode']")
        postcode_field.send_keys("69-997")
        time.sleep(1)

        city_field = self.driver.find_element(By.XPATH, "//input[@id='field-city']")
        city_field.send_keys("Wegorzewo")
        time.sleep(1)

        continue_button = next(filter(lambda x: x.is_displayed(), self.driver.find_elements(By.XPATH, "//button[@class='continue btn btn-primary float-xs-right']")), None)
        continue_button.click()
        time.sleep(1)

        continue_button = self.driver.find_element(By.XPATH, "//button[@class='continue btn btn-primary float-xs-right' and @name='confirmDeliveryOption']")
        continue_button.click()
        time.sleep(1)

        payment_radio = self.driver.find_element(By.XPATH, "//input[@id='payment-option-1']")
        payment_radio.click()
        time.sleep(1)

        terms_checkbox = self.driver.find_element(By.XPATH, "//input[@id='conditions_to_approve[terms-and-conditions]']")
        terms_checkbox.click()
        time.sleep(1)

        order_button = self.driver.find_element(By.XPATH, "//div[@id='payment-confirmation']/div/button")
        order_button.click()
        time.sleep(1)

        return self.driver.find_element(By.XPATH, "//li[@id='order-reference-value']").text.split(":")[-1].strip()

    def check_status(self, order_id):
        self.driver.get("https://localhost:17188/historia-zamowien")
        time.sleep(2.5)

        order_row = self.driver.find_element(By.XPATH, f"//th[contains(text(), {order_id})]/..")
        details_url = order_row.find_element(By.XPATH, "//a[@data-link-action='view-order-details']").get_property("href")

        self.driver.get(details_url)
        time.sleep(2.5)

        logging.info("Log out")
        logout_button = self.driver.find_element(By.XPATH, "//a[@class='logout hidden-sm-down']")
        logout_button.click()
        time.sleep(2.5)


if __name__ == "__main__":
    unittest.main()

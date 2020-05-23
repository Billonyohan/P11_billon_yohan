import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 


class FormContactTest(unittest.TestCase):

    def setUp(self):
        self.selenium = webdriver.Chrome("/Users/macbookair/Documents/chromedriver")

    def test_form_contact_send(self):
        selenium = self.selenium
        selenium.get('https://purbeurreapp.herokuapp.com')
        username = selenium.find_element_by_id('id_user')
        mail = selenium.find_element_by_id('id_email')
        message = selenium.find_element_by_id('id_message')
        submit = selenium.find_element_by_name('send')
        username.send_keys('Aloe45')
        mail.send_keys('purbeurre.paris@gmail.com')
        message.send_keys('Ca marche !')
        submit.send_keys(Keys.RETURN)


    def tearDown(self):
        self.selenium.close()

if __name__ == "__main__":
    unittest.main()

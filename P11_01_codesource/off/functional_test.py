from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys



selenium = webdriver.Chrome("/Users/macbookair/Documents/chromedriver")
selenium.get('https://purbeurreapp.herokuapp.com')
#find the form element
username = selenium.find_element_by_id('id_user')
mail = selenium.find_element_by_id('id_email')
message = selenium.find_element_by_id('id_message')
submit = selenium.find_element_by_name('send')

#Fill the form with data
username.send_keys('Aloe45')
mail.send_keys('purbeurre.paris@gmail.com')
message.send_keys('Ca marche !')

#submitting the form
submit.send_keys(Keys.RETURN)
selenium.quit()
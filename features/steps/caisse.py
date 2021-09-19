from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

@given(u'I navigate to caisse page')
def step_impl(context):
    context.browser.get('http://127.0.0.1:5000/caisse/spicerie')

### Scenario: Success test to search product ###
@given(u'I click on search button')
def step_impl(context):
    context.browser.find_element_by_id("search_product").click()

@when (u'I put a product name in modal dialog')
def step_impl(context):
    context.browser.find_element_by_id("search_product_Modal")
    context.browser.find_element_by_id("search_input").send_keys('Banane')
    context.browser.find_element_by_id("valid_search_product").click()

@then (u'I can add to the cart among the results in the modal dialog a product and a quantity')
def step_impl(context):
    context.browser.find_element_by_id("successModal")
    el = WebDriverWait(context.browser, 60).until(EC.element_to_be_clickable((By.XPATH, """//*[@id="table_achats"]/tbody/tr[1]/td[2]""")))
    el.click()
    context.browser.find_element(By.XPATH, """//*[@id="successModal"]/div/div/div[2]/form/div[2]/div[2]/input""").send_keys('2')
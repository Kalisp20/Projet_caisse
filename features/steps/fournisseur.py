from behave import given, when, then
import mysql.connector
from mysql.connector import errorcode
import time 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains


@given(u'I navigate to supplier page')
def step_impl(context):
    """
        Navigate to login page and as the web server will run in local when we run
        end to end tests using behave, the url will be http://127.0.0.1:5000/index/spicerie
    """
    context.browser.get('http://127.0.0.1:5000/test/spicerie')

@when(u'I click on consult button')
def step_impl(context):
    """
        Find the input button on the html page which has value = Rechercher
        and invoke .click()
    """
    context.browser.find_element_by_id('Consulter').click()

@then(u'Success modal open')
def step_impl(context):
    time.sleep(5)
    context.browser.find_element_by_id('successModal')

@then(u'Click to consult supplier')
def step_impl(context):
    WebDriverWait(context.browser, 10).until(EC.element_to_be_clickable((By.ID, 'consult_supplier'))).click()
    context.browser.find_element_by_id('close_consult').click()

@then(u'View table Fournisseur')
def step_impl(context):
    assert len (context.browser.find_elements_by_xpath("//*[@id='sample_data']/tbody/tr")) >= 1
    assert len (context.browser.find_elements_by_xpath("//*[@id='sample_data']/tbody/tr/td")) == 9


## Scenario: Success delete a supplier ##
@given(u'I navigate to consult supplier page')
def step_impl(context):
    """
        Navigate to login page and as the web server will run in local when we run
        end to end tests using behave, the url will be http://127.0.0.1:5000/index/spicerie
    """
    context.browser.get('http://127.0.0.1:5000/test2/spicerie')

@when(u'I click to garbage button')
def step_impl(context): 
    #first make overlay element invisible 
    overlay = context.browser.find_element_by_class_name("modal-backdrop")
    context.browser.execute_script("arguments[0].style.display = 'none'", overlay)
    WebDriverWait(context.browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="successModal"]/div/div/div[1]/button'))).click()
    
    context.browser.find_element_by_xpath('//*[@id="DeleteButton"]').click()

@then(u'I confirm how to delete')
def step_impl(context):
    context.browser.find_element_by_xpath('/html/body/div[3]/div/div/div[2]/form/div[2]/button[2]').click()
    

@when(u'I input email and tel')
def step_impl(context):

    WebDriverWait(context.browser, 10).until(EC.element_to_be_clickable((By.ID, 'close_consult'))).click()
    el = WebDriverWait(context.browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="sample_data"]/tbody/tr/td[7]')))
    el.click()
    ActionChains(context.browser).move_to_element(el).click(el).send_keys('0909090909')

    WebDriverWait(context.browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'editable-buttons'))).click()


@then(u'I update table fournisseur')
def step_impl(context):
    
    conn = mysql.connector.connect(user='root', password='virtuel1',host='127.0.0.1', database='spicerie')
    cur = conn.cursor(dictionary=True)
    sql= "SELECT * FROM Fournisseur"
    cur.execute(sql)
    print(cur.fetchall())

    context.browser.find_element_by_id('exampleModal1')


@when(u'I click on search button')
def step_impl(context):
    """
        Find the input button on the html page which has value = Rechercher
        and invoke .click()
    """
    search = context.browser.find_element_by_id('Rechercher')
    print(search)
    search.click()
    #context.browser.find_element_by_link_text('Rechercher').click()

@then(u'Dialog modal open')
def step_impl(context):
    context.browser.find_element_by_id('exampleModal1')

@when(u'I search a supplier ARMOR FRUIT')
def step_impl(context):
    context.browser.find_element_by_name('search_fournisseurs').send_keys('ARMOR FRUIT')

@then(u'I click to submit button')
def step_impl(context):
    context.browser.find_element_by_id("submit").click()
  
@then(u'Success message to invite to go select a supplier')
def step_impl(context):
    #WebDriverWait(context.browser, 20).until(EC.element_to_be_clickable((By.ID, "select_supplier"))).click()
    context.browser.find_element_by_id("select_supplier").click()
    time.sleep(2)
    context.browser.find_element_by_id("close").click()

@when(u"I search a supplier '<<<<'")
def step_impl(context):
    context.browser.find_element_by_name('search_fournisseurs').send_keys('<<<<')

@then(u'No result view')
def step_impl(context):
    assert context.browser.find_element_by_id('failModal')

@then(u'I click to close button')
def step_impl(context):
    context.browser.find_element_by_id("close").click()

@then(u'Dialog modal close')
def step_impl(context):
    assert context.browser.find_element_by_id('exampleModal1') 


@then(u'Result view')
def step_impl(context):
    assert len (context.browser.find_elements_by_xpath("//*[@id='table_achats']/tbody/tr")) >= 1
    assert len (context.browser.find_elements_by_xpath("//*[@id='table_achats']/tbody/tr[2]/td")) == 8


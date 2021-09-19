from behave import given, when, then
import mysql.connector
from mysql.connector import errorcode
import time 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

@given(u'I navigate to stock page')
def step_impl(context):
    """
        Navigate to login page and as the web server will run in local when we run
        end to end tests using behave, the url will be http://127.0.0.1:5000/index/spicerie
    """
    context.browser.get('http://127.0.0.1:5000/stock/spicerie')

### Scenario: Success test to consult stock ###
@given(u'I click on consult button')
def step_impl(context):
    """
        Find the input button on the html page which has value = bills
        and invoke .click()
    """
    context.browser.find_element_by_id("consult").click()

@then (u'I navigate to stock view')
def step_impl(context):
    context.browser.find_element_by_id("sample_data")

### Scenario: Success test for bills download ###
@given(u'I click on bills button')
def step_impl(context):
    """
        Find the input button on the html page which has value = bills
        and invoke .click()
    """
    context.browser.find_element_by_id("bills").click()

@when(u'I select a supplier and date, taxe, marge, and bills in modal dialog')
def step_impl(context):
    """
        Find the input button on the html page which has value = Rechercher
        and invoke .click()
    """
    context.browser.find_element_by_id("exampleModal1")

    # Select Supplier
    select_supplier = context.browser.find_element(By.NAME,'id_f')
    select_object_supplier = Select(select_supplier)
    select_object_supplier.select_by_visible_text('FFFOLIES')

    #Select Categorie
    select_categ = context.browser.find_element(By.NAME,'categ')
    select_object_categ = Select(select_categ)
    select_object_categ.select_by_visible_text('Fruits & Légumes')
   
    #Select DateTime
    #context.browser.find_element(By.ID,"datetimepicker1").click()
    elem = context.browser.find_element_by_name("datetimepicker1")
    elem.send_keys("2021-09-01 00:00:00")

    condition = EC.visibility_of_element_located((By.ID,"datetimepicker1"))

    #Select Marge
    context.browser.find_element(By.NAME,"marge").send_keys('30')
    
    #Select Taxe
    select_taxe = context.browser.find_element(By.NAME,"taxe")
    select_object_taxe = Select(select_taxe)
    select_object_taxe.select_by_value('5.5')

    # Select File
    context.browser.find_element(By.NAME,"file").send_keys('/Users/hanane/Downloads/startbootstrap-stylish-portfolio-gh-pages/ARMORFRUITS-Facture-840787.pdf')

    #Validate input
    context.browser.find_element(By.NAME,"PDF").click()
    time.sleep(2)

@then(u'Success dialog open')
def step_impl(context):
   context.browser.find_element_by_id("successModal")
   context.browser.find_element_by_id("go_view").click()


###  Failure test for bills download ###
@when(u'I miss select a supplier or date, taxe, marge, and bills in modal dialog')
def step_impl(context):
    """
        Find the input button on the html page which has value = Rechercher
        and invoke .click()
    """
    context.browser.find_element_by_id("exampleModal1")

    #Select Categorie
    select_categ = context.browser.find_element(By.NAME,'categ')
    select_object_categ = Select(select_categ)
    select_object_categ.select_by_visible_text('Fruits & Légumes')
   
    #Select DateTime
    #context.browser.find_element(By.ID,"datetimepicker1").click()
    elem = context.browser.find_element_by_name("datetimepicker1")
    elem.send_keys("2021-09-01 00:00:00")

    condition = EC.visibility_of_element_located((By.ID,"datetimepicker1"))

    #Select Marge
    context.browser.find_element(By.NAME,"marge").send_keys('30')
    
    #Select Taxe
    select_taxe = context.browser.find_element(By.NAME,"taxe")
    select_object_taxe = Select(select_taxe)
    select_object_taxe.select_by_value('5.5')

    #Validate input
    context.browser.find_element(By.NAME,"PDF").click()
    time.sleep(2)

@then(u"Input is failed and modal dialog don't disappear")
def step_impl(context):
   context.browser.find_element_by_id("exampleModal1")


## Scenario: Success test to add a product in stock 
@given(u'I click on add product button')
def step_impl(context):
    """
        Find the input button on the html page which has value = bills
        and invoke .click()
    """
    context.browser.find_element_by_id("add_product").click()

@when(u'I select a supplier and date, taxe, marge, and info product')
def step_impl(context):
    """
        Find the input button on the html page which has value = Rechercher
        and invoke .click()
    """
    context.browser.find_element_by_id("exampleModal")

    # Select Supplier
    select_supplier = context.browser.find_element(By.NAME,'id_f')
    select_object_supplier = Select(select_supplier)
    select_object_supplier.select_by_visible_text('FFFOLIES')

    #Select Categorie
    select_categ = context.browser.find_element(By.NAME,'categ')
    select_object_categ = Select(select_categ)
    select_object_categ.select_by_visible_text('Fruits & Légumes')
   
    #Select DateTime
    #context.browser.find_element(By.ID,"datetimepicker1").click()
    elem = context.browser.find_element_by_name("datetimepicker2")
    elem.send_keys("2021-09-01 00:00:00")

    condition = EC.visibility_of_element_located((By.ID,"datetimepicker2"))

    #Select Lot
    context.browser.find_element(By.NAME,"lot").send_keys(int(4000))

    #Select Colis
    context.browser.find_element(By.NAME,"colis").send_keys('4')

    #Select Taxe
    select_taxe = context.browser.find_element(By.NAME,"taxe")
    select_object_taxe = Select(select_taxe)
    select_object_taxe.select_by_value('5.5')

    #Select Produit
    context.browser.find_element(By.NAME,"prod").send_keys('test')

    #Select Description produit
    context.browser.find_element(By.NAME,"d_produit").send_keys('test_des')

    #Select Origine
    context.browser.find_element(By.NAME,"ori").send_keys('Maroc')
    
    #Select Quantité
    context.browser.find_element(By.NAME,"quantity").send_keys('5')
    
    #Select Unité
    select_unity= context.browser.find_element(By.NAME,"unity")
    select_object_unity = Select(select_unity)
    select_object_unity.select_by_visible_text('K')
    
    #Select Price
    context.browser.find_element(By.NAME,"price").send_keys('100')

    time.sleep(2)
    #Select Marge
    context.browser.find_element(By.NAME,"marge_manuel").send_keys(int(30))

    #Validate input
    context.browser.find_element(By.NAME,"Manuel").click()

### Scenario: Failure test to add a product in stock  ###
@when(u'I miss select a supplier or date, taxe, marge, or info product')
def step_impl(context):
    """
        Find the input button on the html page which has value = Rechercher
        and invoke .click()
    """
    context.browser.find_element_by_id("exampleModal")


    #Select Categorie
    select_categ = context.browser.find_element(By.NAME,'categ')
    select_object_categ = Select(select_categ)
    select_object_categ.select_by_visible_text('Fruits & Légumes')
   
    #Select DateTime
    #context.browser.find_element(By.ID,"datetimepicker1").click()
    elem = context.browser.find_element_by_name("datetimepicker2")
    elem.send_keys("2021-09-01 00:00:00")

    condition = EC.visibility_of_element_located((By.ID,"datetimepicker2"))

    #Select Lot
    context.browser.find_element(By.NAME,"lot").send_keys(int(4000))

    #Select Colis
    context.browser.find_element(By.NAME,"colis").send_keys('4')
    
    #Select Taxe
    select_taxe = context.browser.find_element(By.NAME,"taxe")
    select_object_taxe = Select(select_taxe)
    select_object_taxe.select_by_value('5.5')

    #Select Produit
    context.browser.find_element(By.NAME,"prod").send_keys('test')

    #Select Description produit
    context.browser.find_element(By.NAME,"d_produit").send_keys('test_des')

    #Select Origine
    context.browser.find_element(By.NAME,"ori").send_keys('Maroc')
    
    #Select Quantité
    context.browser.find_element(By.NAME,"quantity").send_keys('5')
    
    #Select Unité
    select_unity= context.browser.find_element(By.NAME,"unity")
    select_object_unity = Select(select_unity)
    select_object_unity.select_by_visible_text('K')
    
    #Select Price
    context.browser.find_element(By.NAME,"price").send_keys('100')

    time.sleep(2)
    #Select Marge
    context.browser.find_element(By.NAME,"marge_manuel").send_keys(int(30))

    #Validate input
    context.browser.find_element(By.NAME,"Manuel").click()

@when(u'I select day conservation')
def step_impl(context):
    context.browser.find_element(By.ID,"go_view").click()
    context.browser.find_element(By.XPATH,"""//*[@id="successModal"]/div/div/div[1]/button""").click()
    #WebDriverWait(context.browser, 90).until(EC.element_to_be_clickable((By.ID, 'close_success_modal'))).click()
    overlay = context.browser.find_element_by_class_name("modal-backdrop")
    context.browser.execute_script("arguments[0].style.display = 'none'", overlay)

    el = WebDriverWait(context.browser, 60).until(EC.element_to_be_clickable((By.ID, 'jours_conservation')))
    el.click()
    ActionChains(context.browser).move_to_element(el).click(el).send_keys('2')

    #SearchInput= context.browser.find_element(By.ID,"jours_conservation")
    #SearchInput.clear()
    #SearchInput.send_keys("2")
    time.sleep(3)
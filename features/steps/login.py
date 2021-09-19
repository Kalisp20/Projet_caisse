from behave import given, when, then

from src.database import *
import mysql.connector
from mysql.connector import errorcode
import app

@given(u'I navigate to login page')
def step_impl(context):
    """
        Navigate to login page and as the web server will run in local when we run
        end to end tests using behave, the url will be http://127.0.0.1:5000/
    """
    context.browser.get('http://127.0.0.1:5000')


@given(u'I enter valid username and password')
def step_impl(context):
    """
        Find the html element using the name attribute and input the required data
        Here entering validusername and validpassword as the step definition says:
        I enter valid username and password
    """
    context.browser.find_element_by_name('name').send_keys('spicerie')
    context.browser.find_element_by_name('email').send_keys('hanane.simple@gmail.com')
    context.browser.find_element_by_name('password').send_keys('TESTOK')
    
@when(u'I click on Submit button')
def step_impl(context):
    """
        Find the input button on the html page which has value = Submit
        and invoke .click()
    """
    context.browser.find_element_by_id("submit").click()
    


@then(u'database login is successful')
def step_impl(context):
    """
        If the login is successful we will be redirected to http://127.0.0.1:5000/index
        and also see the message "Login successful !!" on that page
    """

    assert context.browser.current_url == 'http://127.0.0.1:5000/index/spicerie'

@then(u'login is successful')
def step_impl(context):
    """
        If the login is successful we will be redirected to http://127.0.0.1:5000/index
        and also see the message "Login successful !!" on that page
    """
    conn = mysql.connector.connect(user='root', password='virtuel1',host='127.0.0.1', database='Spicerie')
    cur = conn.cursor(dictionary=True)
    print(cur.execute("SELECT * FROM  Activity ORDER BY ouverture DESC LIMIT 1"))
    print(cur.fetchall())
    assert context.browser.current_url == 'http://127.0.0.1:5000/index/spicerie'
    #assert 'spicerie' in context.browser.page_source



@given(u'I enter invalid username or password')
def step_impl(context):
    """
        Find the html element using the name attribute and input the required data
        Here entering invalidusername and invalidpassword as the step definition says:
        I enter invalid username or password
    """
    context.browser.find_element_by_name('name').send_keys('invalidusername')
    context.browser.find_element_by_name('email').send_keys('invalidemail')
    context.browser.find_element_by_name('password').send_keys('invalidpassword')


@then(u'login fails')
def step_impl(context):
    """
        If the login is successful we will not be redirected to http://127.0.0.1:5000/index/spicerie
        but will be on the same page: http://127.0.0.1:5000/
        and also see the message "Welcome Back!" on that page
    """
    # Alert invalid user
    assert context.browser.find_element_by_xpath('/html/body/div/div[1]')
    # Page login 
    assert context.browser.current_url == 'http://127.0.0.1:5000/'
    assert 'Welcome Back!' in context.browser.page_source
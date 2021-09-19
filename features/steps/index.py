from behave import given, when, then


@given(u'I navigate to Home page')
def step_impl(context):
    """
        Navigate to login page and as the web server will run in local when we run
        end to end tests using behave, the url will be http://127.0.0.1:5000/index/spicerie
    """
    context.browser.get('http://127.0.0.1:5000/index/spicerie')

    
@when(u'I click on Caisse')
def step_impl(context):
    """
        Find the input button on the html page which has value = Caisse
        and invoke .click()
    """
    context.browser.find_element_by_id('Caisse').click()
    


@then(u'I navigate to Caisse page')
def step_impl(context):
    """
        If the login is successful we will be redirected to http://127.0.0.1:5000/caisse/spicerie
    """

    assert context.browser.current_url == 'http://127.0.0.1:5000/caisse/spicerie'


@when(u'I click on Fournisseur')
def step_impl(context):
    """
        Find the input button on the index page which has value = Fournisseur
        and invoke .click()
    """
    context.browser.get('http://127.0.0.1:5000/index/spicerie')
    context.browser.find_element_by_id("Fournisseur").click()
    

@then(u'I navigate to Fournisseur page')
def step_impl(context):
    """
        If the login is successful we will be redirected to http://127.0.0.1:5000/test/spicerie
    """
    assert context.browser.current_url == 'http://127.0.0.1:5000/test/spicerie'

# Test Dashboard Link
@when(u'I click on Dashboard')
def step_impl(context):
    """
        Find the input button on the index page which has value = Dashboard
        and invoke .click()
    """
    context.browser.get('http://127.0.0.1:5000/index/spicerie')
    context.browser.find_element_by_id("Dashboard").click()
    

@then(u'I navigate to Dashboard page')
def step_impl(context):
    """
        If the login is successful we will be redirected to http://127.0.0.1:5000/index
    """

    assert context.browser.current_url == 'http://127.0.0.1:5000/dashboard/spicerie'

@when(u'I click on Stock')
def step_impl(context):
    """
        Find the input button on the index page which has value = Stock
        and invoke .click()
    """
    context.browser.get('http://127.0.0.1:5000/index/spicerie')
    context.browser.find_element_by_id("Stock").click()
    

@then(u'I navigate to Stock page')
def step_impl(context):
    """
        If the login is successful we will be redirected to http://127.0.0.1:5000/index
    """
    assert context.browser.current_url == 'http://127.0.0.1:5000/stock/spicerie'

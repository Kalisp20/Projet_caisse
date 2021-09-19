import os
import tempfile
from behave import fixture, use_fixture
from selenium import webdriver
import tempfile
import app 

def before_all(context):

    context.browser = webdriver.Firefox()
    context.browser.set_page_load_timeout(time_to_wait=200)
    

def after_all(context):
    context.browser.quit()